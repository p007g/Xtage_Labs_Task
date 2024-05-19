from django.shortcuts import render
from django.http import JsonResponse
from .services.utils import GoogleBooksClient  # The function we wrote earlier

from rest_framework import viewsets
from .models import BookRecommendation
from .serializers import RecommendationSerializer

# Create your views here.

# to get the GoogleAPIKey request--
def search_books(request):
    # query = "harry potter"
    query = request.GET.get('q', '')
    results = GoogleBooksClient.search_books(query)
    return JsonResponse(results)


# serialize the model data with the APIs
class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = BookRecommendation.objects.all()
    serializer_class = RecommendationSerializer