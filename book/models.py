from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class IndustryIdentifier(models.Model):
    identifier_type = models.CharField(max_length=10)
    identifier = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.identifier_type, self.identifier)


class ImageLink(models.Model):
    small_thumbnail = models.URLField()
    thumbnail = models.URLField()

    def __str__(self):
        return self.thumbnail


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, blank=True)
    published_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    industry_identifiers = models.ManyToManyField(
        IndustryIdentifier, blank=True)
    page_count = models.IntegerField(null=True, blank=True)
    image_links = models.ManyToManyField(ImageLink, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.title
