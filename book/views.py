import datetime
import json
import requests
from django.shortcuts import render
from rest_framework import generics, filters
from .forms import AddBookForm, ImportBooksForm, SearchBookForm
from .forms import NewAuthorFormset, NewIndustryIdentifierFormset
from .models import Author, IndustryIdentifier, ImageLink, Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
    '''Django REST Framework configuration'''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'authors__name', 'language', 'published_date']


def add_book(request):
    '''Function gets data from request.POST and saves it to database as Book.
    Also saves optional data from manually added author and/or book inudstry identifier
    '''
    msg = ''
    if request.method == 'POST':
        model_form = AddBookForm(request.POST)
        new_author_form = NewAuthorFormset(request.POST)
        new_industry_identifier_form = NewIndustryIdentifierFormset(
            request.POST)
        if model_form.is_valid() and new_author_form.is_valid() and \
            new_industry_identifier_form.is_valid():
            new_book = model_form.save()
            msg = 'Book successfully added'
            if model_form.cleaned_data.get('new_image_link_thumbnail') and \
                model_form.cleaned_data.get('new_image_link_small_thumbnail'):

                new_image_link_pair, created = ImageLink.objects.get_or_create(
                    thumbnail=model_form.cleaned_data.get(
                        'new_image_link_thumbnail'), small_thumbnail=model_form.cleaned_data.get(
                            'new_image_link_small_thumbnail'))
                new_book.image_links.add(new_image_link_pair)
            if new_author_form.is_valid():
                for f in new_author_form:
                    n = f.cleaned_data.get('name')
                    if n:
                        new_author, created = Author.objects.get_or_create(
                            name=n)
                        new_book.authors.add(new_author)
            if new_industry_identifier_form.is_valid():
                for i in new_industry_identifier_form:
                    n = i.cleaned_data.get('industry_identifier_type')
                    m = i.cleaned_data.get('industry_identifier')
                    if n and m:
                        new_industry_identifier_pair, created = IndustryIdentifier.objects.get_or_create(
                            identifier_type=n, identifier=m)
                        new_book.industry_identifiers.add(
                            new_industry_identifier_pair)
    form = AddBookForm()
    new_author_formset = NewAuthorFormset(request.GET or None)
    new_industry_identifier_formset = NewIndustryIdentifierFormset(
        request.GET or None)
    return render(request, 'book/add.html', {'form': form, 'new_author_formset': new_author_formset, 'new_industry_identifier_formset': new_industry_identifier_formset, 'msg': msg})


def search(request):
    '''Function prepares kwargs for filtering books and returns filtered matches to template'''
    form = SearchBookForm(request.POST)
    if request.method == 'POST':
        kwargs = {}
        if form.is_valid():
            for f in form.cleaned_data:
                if len(form.cleaned_data[f]) > 0:
                    if f == 'title':
                        kwargs['title__icontains'] = form.cleaned_data[f]
                    if f == 'authors':
                        kwargs['authors__name__icontains'] = form.cleaned_data[f]
                    if f == 'language':
                        kwargs['language__icontains'] = form.cleaned_data[f]
            if len(form.cleaned_data['published_date_from']) >= 4 and len(form.cleaned_data['published_date_to']) >= 4:
                kwargs['published_date__range'] = [form.cleaned_data['published_date_from'], form.cleaned_data['published_date_to']]
            elif len(form.cleaned_data['published_date_from']) >= 4 and len(form.cleaned_data['published_date_to']) < 4:
                kwargs['published_date__gte'] = form.cleaned_data['published_date_from']
            elif len(form.cleaned_data['published_date_from']) < 4 and len(form.cleaned_data['published_date_to']) >= 4:
                kwargs['published_date__lte'] = form.cleaned_data['published_date_to']
            found_books = Book.objects.filter(**kwargs)
        return render(request, 'book/search.html', {'form': form, 'found_books': found_books})
    return render(request, 'book/search.html', {'form': form})


def import_books(request):
    '''Function gets data from request.POST and prepares it for Google API request. 
    Next it calls save_imported_books() to actually download and save data to database.
    Finally it returns saved books Queryset to template.
    '''
    imported_books = []
    if request.method == 'POST':
        api_request_params = ''
        import_book_form = ImportBooksForm(request.POST)
        if import_book_form.is_valid():
            for f in import_book_form:
                if import_book_form.cleaned_data.get(f.name):
                    api_request_params += '{}:{}+'.format(
                        f.name, import_book_form.cleaned_data.get(f.name))
            imported_books = save_imported_books(api_request_params)
    import_book_form = ImportBooksForm()
    return render(request, 'book/import.html', {'imported_books': imported_books, 'form': import_book_form})


def string_to_date(published_date):
    '''Function tries to convert string to datetime object. 
    If given string is in correct date format datetime object is returned,
    otherwise it returns None.
    '''
    if published_date:
        try:
            int(published_date.replace('-', ''))
        except ValueError:
            return None
        # YYYY-MM-DD
        if len(published_date) == 10 and len(published_date.split('-')[0]) == 4:
            published_date = datetime.datetime.strptime(
                published_date, '%Y-%m-%d').date()
        # YYYY-MM
        elif len(published_date) == 7 and len(published_date.split('-')[0]) == 4:
            published_date = datetime.datetime.strptime(
                published_date, '%Y-%m').date()
        # YYYY
        elif len(published_date) == 4:
            published_date = datetime.datetime.strptime(
                published_date, '%Y').date()
        else:
            return None
        return published_date
    return None


def download_data_from_gapi(api_request_params):
    '''Function downloads data from Google API filtered by given parameters'''
    g_api_url = 'https://www.googleapis.com/books/v1/volumes?q='
    response = requests.get(g_api_url + api_request_params)
    api_response = json.loads(response.text)
    return api_response



def save_imported_books(api_request_params):
    '''Function processes and saves data from Google API to database as Book.'''
    api_response = download_data_from_gapi(api_request_params)
    if api_response.get('items'):
        imported_books = []
        for i in api_response['items']:
            title = i.get('volumeInfo', {}).get('title')
            published_date = i.get('volumeInfo', {}).get('publishedDate')
            page_count = i.get('volumeInfo', {}).get('pageCount')
            page_count = i.get('volumeInfo', {}).get('pageCount')
            language = i.get('volumeInfo', {}).get('language')
            book = Book.objects.create(title=title, published_date=string_to_date(
                published_date), page_count=page_count, language=language)
            try:
                small_thumbnail = i.get('volumeInfo', {}).get(
                    'imageLinks').get('smallThumbnail')
                thumbnail = i.get('volumeInfo', {}).get(
                    'imageLinks').get('thumbnail')
                image_links, created = ImageLink.objects.get_or_create(
                    small_thumbnail=small_thumbnail, thumbnail=thumbnail)
                book.image_links.add(image_links)
            except AttributeError:
                pass
            authors = i.get('volumeInfo', {}).get('authors')
            if authors:
                for a in authors:
                    new_author, created = Author.objects.get_or_create(name=a)
                    book.authors.add(new_author)
            industry_identifiers = i.get(
                'volumeInfo', {}).get('industryIdentifiers')
            if industry_identifiers:
                for ii in industry_identifiers:
                    identifier_type = ii.get('type', None)
                    identifier = ii.get('identifier', None)
                    new_industry_identifier, created = IndustryIdentifier.objects.get_or_create(
                        identifier_type=identifier_type, identifier=identifier)
                    book.industry_identifiers.add(new_industry_identifier)
            imported_books.append(book)
    return imported_books
