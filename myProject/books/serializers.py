from rest_framework import serializers
from .models import BookRecommendation

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRecommendation
        fields = '__all__'
