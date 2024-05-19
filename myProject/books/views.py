from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services.utils import GoogleBooksClient  # The function we wrote earlier

from rest_framework import viewsets
from .models import BookRecommendation
from .serializers import RecommendationSerializer


def redirect_to_books(request):
    return redirect('/books/')

# Create your views here.

def index(request):
    return render(request, 'search_results.html')

def handler404(request, exception):
    return render(request, '404.html', status=404)


# to get the GoogleAPIKey request--
def search_books(request):
    query = request.GET.get('q', '')
    results = GoogleBooksClient.search_books(query)
    return JsonResponse(results)


# serialize the model data with the APIs
class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = BookRecommendation.objects.all()
    serializer_class = RecommendationSerializer