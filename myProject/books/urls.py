from django.urls import path
from . import views



urlpatterns = [
    path('search/', views.search_books, name='search_books'),
]

