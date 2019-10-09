from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.search, name='search'),
    path('add', views.add_book, name='add_book'),
    path('import/', views.import_books, name='import_books'),
    path('api/', views.BookList.as_view(), name='api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
