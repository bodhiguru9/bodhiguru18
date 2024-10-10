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
from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

from words.models import PowerWords, NegativeWords, Words 

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
    permission_classes = [AllowAny]  # No authentication required

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sub_competencies.csv"'

        # Create a CSV writer
        writer = csv.writer(response)
        # Write the header row
        writer.writerow(['Sub Competency Name', 'Power Words', 'Power Words Count', 
                         'Negative Words', 'Negative Words Count', 
                         'Emotion Words', 'Emotion Words Count'])

        # Fetch all sub-competencies
        for sub_comp in Sub_Competency.objects.all():
            # Fetch related power words, negative words, and emotion words
            power_words = ', '.join([pw.word.word_name for pw in sub_comp.power_words.all()])
            negative_words = ', '.join([nw.word.word_name for nw in sub_comp.negative_words.all()])
            emotion_words = ', '.join([ew.emotion_word_name for ew in sub_comp.emotion_words.all()])

            # Write data to CSV
            writer.writerow([sub_comp.name, 
                             power_words, sub_comp.power_words.count(),
                             negative_words, sub_comp.negative_words.count(),
                             emotion_words, sub_comp.emotion_words.count()])

        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file.name.endswith('.csv'):
        return Response({"error": "Please upload a CSV file."}, status=400)

    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    next(reader)  # Skip the header row if your CSV contains headers

    for row in reader:
        try:
            sub_competency_name, power_word_names, negative_word_names = row

            # Get or create the SubCompetency
            sub_competency, _ = Sub_Competency.objects.get_or_create(name=sub_competency_name)

            # Process Power Words - append new words to the existing ones
            power_words = power_word_names.split(',')
            for pw_name in power_words:
                pw_name = pw_name.strip().lower()

                # Fetch all entries of Words with the same word_name
                word_objs = Words.objects.filter(word_name=pw_name)

                # Log if there are multiple entries of the same word_name
                if word_objs.count() > 1:
                    print(f"Duplicate word found for power word: {pw_name}")

                # If no entries exist, create one
                if not word_objs.exists():
                    word_obj = Words.objects.create(word_name=pw_name)
                else:
                    # Use the first entry if duplicates exist
                    word_obj = word_objs.first()

                # Get or create PowerWords and associate it with the word
                power_word, _ = PowerWords.objects.get_or_create(word=word_obj)

                # Add the power word to the sub-competency without overwriting existing words
                sub_competency.power_words.add(power_word)

            # Process Negative Words - append new words to the existing ones
            negative_words = negative_word_names.split(',')
            for nw_name in negative_words:
                nw_name = nw_name.strip().lower()

                # Fetch all entries of Words with the same word_name
                word_objs = Words.objects.filter(word_name=nw_name)

                # Log if there are multiple entries of the same word_name
                if word_objs.count() > 1:
                    print(f"Duplicate word found for negative word: {nw_name}")

                # If no entries exist, create one
                if not word_objs.exists():
                    word_obj = Words.objects.create(word_name=nw_name)
                else:
                    # Use the first entry if duplicates exist
                    word_obj = word_objs.first()

                # Get or create NegativeWords and associate it with the word
                negative_word, _ = NegativeWords.objects.get_or_create(word=word_obj)

                # Add the negative word to the sub-competency without overwriting existing words
                sub_competency.negative_words.add(negative_word)

            # Save the updated sub-competency
            sub_competency.save()

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)

    return Response({"success": "CSV uploaded and processed successfully!"})


def csv_upload_page(request):
    return render(request, 'words/uploadcsv.html')    