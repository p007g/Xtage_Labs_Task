from django.shortcuts import render
from django.http import JsonResponse
from .services.utils import GoogleBooksClient  # The function we wrote earlier

# Create your views here.


def search_books(request):
    query = request.GET.get('q', '')
    results = GoogleBooksClient.search_books(query)
    return JsonResponse(results)
