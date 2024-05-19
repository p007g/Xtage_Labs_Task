from django.db import models


# Create your models here.
class BookRecommendation(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.URLField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
