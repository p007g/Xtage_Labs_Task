from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter


# define the router
router = DefaultRouter()
router.register(r'recommendations', views.RecommendationViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_books, name='search_books'),
] + router.urls