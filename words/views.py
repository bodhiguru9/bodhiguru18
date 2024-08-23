from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework import generics, status  
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from words.models import Words, PowerWords, NegativeWords
from words.serializers import WordSerializer, PowerWordsListSerializer, NegativeWordsListSerializer
      
class ProductView(generics.ListCreateAPIView):  
        queryset = Words.objects.all()  
        serializer_class = WordSerializer
      
        def create(self, request, *args, **kwargs):  
            serializer = self.get_serializer(data=request.data, many=True)  
            serializer.is_valid(raise_exception=True)  
      
            try:  
                self.perform_create(serializer)  
                return Response(serializer.data, status=status.HTTP_201_CREATED)  
            except:  
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PowerWordsViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(PowerWords, pk=pk)
    
    @staticmethod
    def get_queryset():
        return PowerWords.objects.all()
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request):
        serializer = PowerWordsListSerializer(self.get_queryset(), many=True)
        
        response = {
            'status': "success",
            'message': "Data Retrieved Successfully",
            'data': serializer.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
class NegativeWordsViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(PowerWords, pk=pk)
    
    @staticmethod
    def get_queryset():
        return NegativeWords.objects.all()
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request):
        serializer = NegativeWordsListSerializer(self.get_queryset(), many=True)
        
        response = {
            'status': "success",
            'message': "Data Retrieved Successfully",
            'data': serializer.data
        }
        
        return Response(response, status=status.HTTP_200_OK)
