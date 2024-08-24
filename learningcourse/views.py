from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from learningcourse.models import LearningCourse, LearningCourseVideo, LearningCourseDocument
from learningcourse.serializers import LearningCourseSerializer, LearningCourseListSerializer
from learningcourse.serializers import LearningCourseVideoSerializer, LearningCourseVideoListSerializer
from learningcourse.serializers import LearningCourseDocumentSerializer, LearningCourseDocumentListSerializer

class LearningCourseViewSet(ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(LearningCourse, pk=pk)
    
    @staticmethod
    def get_queryset():
        return LearningCourse.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = LearningCourseListSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "Learning Course List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = LearningCourseListSerializer(instance)
        response = {
            "status": "success",
            "message": "Learning Course Detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = LearningCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Learning Course Created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": "Learning Course Not Created",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = LearningCourseSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Learning Course Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": "Learning Course Not Updated",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "Learning Course Deleted",
            "data": {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
class LearningCourseVideoViewSet(ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(LearningCourseVideo, pk=pk)
    
    @staticmethod
    def get_queryset():
        return LearningCourseVideo.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = LearningCourseVideoListSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "Learning Course Video List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = LearningCourseVideoListSerializer(instance)
        response = {
            "status": "success",
            "message": "Learning Course Video Detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = LearningCourseVideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Learning Course Video Created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": "Learning Course Video Not Created",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = LearningCourseVideoSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Learning Course Video Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": "Learning Course Video Not Updated",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "Learning Course Video Deleted",
            "data": {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
    
class LearningCourseDocumentViewSet(ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(LearningCourseDocument, pk=pk)
    
    @staticmethod
    def get_queryset():
        return LearningCourseDocument.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = LearningCourseDocumentListSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "Learning Course Document List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = LearningCourseDocumentListSerializer(instance)
        response = {
            "status": "success",
            "message": "Learning Course Document Detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = LearningCourseDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Learning Course Document Created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": "Learning Course Document Not Created",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = LearningCourseDocumentSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Learning Course Document Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": "Learning Course Document Not Updated",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "Learning Course Document Deleted",
            "data": {}
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
