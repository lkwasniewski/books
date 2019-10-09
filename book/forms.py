from django import forms
from django.forms import formset_factory
from .models import Book


class SearchBookForm(forms.Form):
    title = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    authors = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    language = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    published_date_from = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    published_date_to = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))


class NewAuthorForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))


class NewIndustryIdentifierForm(forms.Form):
    industry_identifier_type = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    industry_identifier = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))


class AddBookForm(forms.ModelForm):
    new_image_link_thumbnail = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}))
    new_image_link_small_thumbnail = forms.CharField(
        required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

    class Meta:
        model = Book
        fields = ('title', 'authors', 'published_date',
                  'industry_identifiers', 'page_count', 'image_links', 'language')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'published_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'page_count': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'language': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }


class ImportBooksForm(forms.Form):
    intitle = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is found in the title.')
    inauthor = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is found in the author.')
    inpublisher = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is found in the publisher.')
    subject = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is listed in the category list of the volume.')
    isbn = forms.CharField(required=False, widget=forms.TextInput(attrs={
                           'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is the ISBN number.')
    lccn = forms.CharField(required=False, widget=forms.TextInput(attrs={
                           'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is the Library of Congress Control Number.')
    oclc = forms.CharField(required=False, widget=forms.TextInput(attrs={
                           'class': 'form-control form-control-sm'}), help_text='Returns results where the text following this keyword is the Online Computer Library Center number.')


NewAuthorFormset = formset_factory(NewAuthorForm, extra=1)
NewIndustryIdentifierFormset = formset_factory(
NewIndustryIdentifierForm, extra=2)
