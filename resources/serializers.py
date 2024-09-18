# resources/serializers.py

from rest_framework import serializers
from .models import Resource, TextResouce

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'description', 'thumbnail','youtube_link']

class TextResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextResouce
        fields = '__all__'        
