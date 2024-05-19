# Xtage_Labs_Task
 Develop a backend application that serves as a central hub for a  community-driven platform focused on sharing and exploring book recommendations.

# Book Recommendations Platform


## Features

- Integration with Google Books API to fetch book data
- API endpoints for searching books, submitting new recommendations, and retrieving recommended books
- Dynamic HTML frontend to display book recommendations
- User-friendly interactions including search functionality and likes for recommendations
- Error handling and loading indicators for improved user experience


## Technologies Used

- Django
- Django REST Framework
- JavaScript
- Bootstrap
- Google Books API

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Running the Project](#running-the-project)
4. [API Endpoints](#api-endpoints)
5. [Frontend](#frontend)
6. [Contributing](#contributing)
7. [License](#license)

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment tool (venv, virtualenv, etc.)

### Steps

1. Setting Up the Project
    1. Initialize the Project:

        - Install Django: pip install django
        - Create a new Django project: django-admin startproject myProject
        - Navigate into the project directory: cd myProject
        - Create a new Django app: python manage.py startapp books

    2. Configure the Project:

        - Add the books app to your INSTALLED_APPS in myProject/settings.py.
        - Set up the database (default is SQLite).


2. Integration with Google Books API
    1. Google Books API Client:
        - Install requests: 
        > pip install requests
        - Create a service to interact with the Google Books API.

        ```python 
        import requests

        class GoogleBooksClient:
            
            url = "https://www.googleapis.com/books/v1/volumes"
            API_KEY = "AIzaSyBvM_EvKXT5jaE3D5TNxc6rY9isWOqT-VY"

            @staticmethod
            def search_books(query):
                # query = "harry potter"
                params = {"q": query, "key": GoogleBooksClient.API_KEY}
                response = requests.get(GoogleBooksClient.url, params=params)
                return response.json()
            
            
            @staticmethod
            def get_book(book_id):
                params = {'key': GoogleBooksClient.API_KEY}
                response = requests.get(f"{GoogleBooksClient.url}/{book_id},", params=params)
                return response.json()
        ```

    2. Create Views and URLs for Searching Books:

    ```python
    from django.shortcuts import render
    from django.http import JsonResponse
    from .services.utils import GoogleBooksClient  # The function we wrote earlier


    def search_books(request):
        query = request.GET.get('q', '')
        results = GoogleBooksClient.search_books(query)
        return JsonResponse(results)
    ```

    URLs:

    ```python
    from django.urls import path
    from . import views



    urlpatterns = [
        path('search/', views.search_books, name='search_books'),
    ]
    ```
    3. Include Books URLs in the Project URLs:

    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("books/", include("books.urls")),
    ]
    ```

3. Community Book Recommendtions:
    1. Create Models:

        ```python
        from django.db import models


        # Create your models here.
        class Recommendation(models.Model):
            title = models.CharField(max_length=200)
            author = models.CharField(max_length=200)
            description = models.TextField()
            cover_image = models.URLField()
            rating = models.FloatField()
            created_at = models.DateTimeField(auto_now_add=True)

        ```

    2. Create Serializers:

        ```python
        from rest_framework import serializers
        from .models import Recommendation

        class RecommendationSerializer(serializers.ModelSerializer):
            class Meta:
                model = Recommendation
                fields = '__all__'
        ```

    3. Create views and URLs:

        ```python
        from django.shortcuts import render
        from django.http import JsonResponse
        from .services.utils import GoogleBooksClient  # The function we wrote earlier

        from rest_framework import viewsets
        from .models import BookRecommendation
        from .serializers import RecommendationSerializer


        # to get the GoogleAPIKey request--
        def search(request):
            query = request.GET.get('q', '')
            results = GoogleBooksClient.search_books(query)
            return JsonResponse(results)


        # serialize the model data with the APIs
        class RecommendationViewSet(viewsets.ModelViewSet):
            queryset = BookRecommendation.objects.all()
            serializer_class = RecommendationSerializer
        ```
        - urls:
        ```python
        from django.urls import path
        from . import views

        from rest_framework.routers import DefaultRouter


        # define the router
        router = DefaultRouter()
        router.register(r'recommendations', views.RecommendationViewSet)


        urlpatterns = [
            path('search/', views.search, name='search'),
        ] + router.urls
        ```

    4. Add REST framework to settings in myProject:

        ```python
        EXTERNAL_APPS = [
        "books",
        "rest_framework",
        ]

        INSTALLED_APPS+=EXTERNAL_APPS

        -- Optionally, add REST framework settings
        REST_FRAMEWORK = {
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
            ),
            'DEFAULT_PARSER_CLASSES': (
                'rest_framework.parsers.JSONParser',
            )
        }
        ```