from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from competency.models import Competency
from competency.serializers import CompetencyListSerializer

class CompetencyViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Competency, pk=pk)
    
    @staticmethod
    def get_queryset():
        return Competency.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CompetencyListSerializer(queryset, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Competency List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
