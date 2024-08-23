from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from industry.models import Industry
from industry.serializers import IndustrySerializer



class IndustryViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Industry, id=pk)
    
    @staticmethod
    def get_queryset():
        return Industry.objects.all()
    
    def list(self, request):
        serializer_data = IndustrySerializer(self.get_queryset(), many=True).data
        response = {
            'status': 'Success',
            'message': "Industry has been successfully retrieved.",
            'data': serializer_data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'status': 'Success',
            'message': 'Industry has been successfully retrieved.',
            'data': IndustrySerializer(self.get_object(pk)).data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data = self.request.data
        data = {
            'name': request_data.get('name'),
            'description': request_data.get('description'),
        }
        
        serializer = IndustrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'message': 'Industry has been successfully created.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'Failed',
            'message': 'Industry creation failed.',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        request_data = self.request.data
        
        data = {
            'name': request_data.get('name', instance.name),
            'description': request_data.get('description', instance.description),
        }
        
        serializer = IndustrySerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'message': 'Industry has been successfully updated.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'Failed',
            'message': 'Industry update failed.',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        instance.delete()

        response = {
            'data': '',
            'message': "Successfully deleted Industry"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
