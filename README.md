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

4. API Creation:

5. Fontend Template Design:

    - HTML template--> (search_results.html)

    ```html

    <!-- books/templates/books/index.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book Recommendations</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            .container {
                width: 80%;
                margin: 0 auto;
                padding: 20px;
            }
            .book {
                border: 1px solid #ccc;
                padding: 15px;
                margin-bottom: 10px;
                display: flex;
                flex-direction: row;
            }
            .book img {
                width: 100px;
                height: 150px;
                margin-right: 20px;
            }
            .book-details {
                flex-grow: 1;
            }
            .search-bar {
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Book Recommendations</h1>
            <div class="search-bar">
                <input type="text" id="searchQuery" placeholder="Search for books...">
                <button onclick="searchBooks()">Search</button>
            </div>
            <div id="bookList"></div>
        </div>

        <script>
            document.addEventListener("DOMContentLoaded", function() {
                fetchRecommendations();
            });

            function fetchRecommendations() {
                fetch('/books/recommendations/')
                    .then(response => response.json())
                    .then(data => {
                        displayBooks(data);
                    })
                    .catch(error => {
                        console.error('Error fetching recommendations:', error);
                    });
            }

            function displayBooks(books) {
                const bookList = document.getElementById('bookList');
                bookList.innerHTML = '';

                books.forEach(book => {
                    const bookElement = document.createElement('div');
                    bookElement.className = 'book';

                    const bookImage = document.createElement('img');
                    bookImage.src = book.cover_image;
                    bookElement.appendChild(bookImage);

                    const bookDetails = document.createElement('div');
                    bookDetails.className = 'book-details';
                    bookElement.appendChild(bookDetails);

                    const bookTitle = document.createElement('h2');
                    bookTitle.textContent = book.title;
                    bookDetails.appendChild(bookTitle);

                    const bookAuthor = document.createElement('p');
                    bookAuthor.textContent = 'Author: ' + book.author;
                    bookDetails.appendChild(bookAuthor);

                    const bookDescription = document.createElement('p');
                    bookDescription.textContent = book.description;
                    bookDetails.appendChild(bookDescription);

                    const bookRating = document.createElement('p');
                    bookRating.textContent = 'Rating: ' + book.rating;
                    bookDetails.appendChild(bookRating);

                    bookList.appendChild(bookElement);
                });
            }

            function searchBooks() {
                const query = document.getElementById('searchQuery').value;
                fetch(`/books/search/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        displayBooks(data.items.map(item => ({
                            title: item.volumeInfo.title,
                            author: item.volumeInfo.authors ? item.volumeInfo.authors.join(', ') : 'Unknown',
                            description: item.volumeInfo.description || 'No description available',
                            cover_image: item.volumeInfo.imageLinks ? item.volumeInfo.imageLinks.thumbnail : '',
                            rating: item.volumeInfo.averageRating || 'No rating'
                        })));
                    })
                    .catch(error => {
                        console.error('Error searching books:', error);
                    });
            }
        </script>
    </body>
    </html>