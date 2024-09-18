from rest_framework import generics, viewsets, status
from .models import Resource, TextResouce
from .serializers import ResourceSerializer

from rest_framework.response import Response
from .serializers import TextResourceSerializer

class TextResourceViewSet(viewsets.ModelViewSet):
    queryset = TextResouce.objects.all()
    serializer_class = TextResourceSerializer

class ResourceListAPIView(generics.ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceCreateAPIView(generics.CreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceUpdateAPIView(generics.UpdateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceDestroyAPIView(generics.DestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer