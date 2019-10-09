from django.contrib import admin
from .models import Author, IndustryIdentifier, ImageLink, Book

admin.site.register(Author)
admin.site.register(IndustryIdentifier)
admin.site.register(ImageLink)
admin.site.register(Book)
