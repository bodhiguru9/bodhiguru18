from rest_framework import generics
from .models import Resource
from .serializers import ResourceSerializer

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