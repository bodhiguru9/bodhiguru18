from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from competency.models import Competency
from competency.serializers import CompetencyListSerializer

import csv
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Sub_Competency
from .serializers import SubCompetencySerializer1
from rest_framework.permissions import AllowAny

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

class SubCompetencyViewSet(viewsets.ModelViewSet):
    queryset = Sub_Competency.objects.all()
    serializer_class = SubCompetencySerializer1
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sub_competencies.csv"'

        # Create a CSV writer
        writer = csv.writer(response)
        # Write the header
        writer.writerow(['Sub Competency Name', 'Power Words', 'Power Words Count', 
                         'Negative Words', 'Negative Words Count', 
                         'Emotion Words', 'Emotion Words Count'])

        # Fetch all sub-competencies
        for sub_comp in Sub_Competency.objects.all():
            # Fetching related power words, negative words, and emotion words
            power_words = ', '.join([word.word for word in sub_comp.power_words.all()])
            negative_words = ', '.join([word.word for word in sub_comp.negative_words.all()])
            emotion_words = ', '.join([word.emotion_word_name for word in sub_comp.emotion_words.all()])

            # Write data to CSV
            writer.writerow([sub_comp.name, power_words, sub_comp.power_words.count(),
                             negative_words, sub_comp.negative_words.count(),
                             emotion_words, sub_comp.emotion_words.count()])

        return response      
