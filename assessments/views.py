from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import pagination
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import UserRightsMapping

from assessments.models import Assessment, AssessmentResult

from assessments.serializers import AssessmentSerializer, AssessmentResultSerializer

from datetime import datetime

import threading

from rest_framework import viewsets
from .models import AssessmentType, Question, Option, Assessment
from .serializers import AssessmentTypeSerializer, QuestionSerializer

from orgss.models import Org  # Import Org model
from rest_framework.decorators import action


from rest_framework.views import APIView



class AssessmentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_queryset():
        return Assessment.objects.all()
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Assessment, pk=pk)
    
    def list(self, request):
        queryset = self.get_queryset()
        try:
            user_rights = UserRightsMapping.objects.filter(user=request.user)
            if user_rights:
                for rights in user_rights:
                    if rights.right.name.lower() == 'approve':
                        queryset = queryset.filter(is_approved=False)
                        break
                    elif rights.right.name.lower() == 'creator':
                        queryset = queryset.filter(is_live=False)
                        break
        except:
            pass
        serializer = AssessmentListSerializer(queryset, many=True)
        response = {
            'status': 'success',
            'message': 'Assessments list',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = AssessmentListSerializer(instance)
        response = {
            'status': 'success',
            'message': 'Assessment details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data = {
            'assessment_type': request.data.get('assessment_type'),
            'access': request.data.get('access')
        }
        if request.data.get('questions'):
            questions_id = [int(id) for id in request.data.get('questions').split(',')]
        
        request_data['questions'] = questions_id
        serializer = AssessmentSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Assessment created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'error',
            'message': 'Invalid data',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        request_data = {
            'assessment_type': request.data.get('assessment_type', instance.assessment_type.id),
            'access': request.data.get('access', instance.access),
            'is_live': request.data.get('is_live', instance.is_live),
            'is_approved': request.data.get('is_approved', instance.is_approved)
        }
        
        if request.data.get('questions'):
            print("adad")
            questions_id = [int(id) for id in request.data.get('questions').split(',')]
            request_data['questions'] = questions_id
        else:
            question_pks = list(instance.questions.values_list('id', flat=True))
            request_data['questions'] = question_pks
        
        serializer = AssessmentSerializer(instance, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Assessment updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'error',
            'message': 'Invalid data',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'success',
            'message': 'Assessment deleted',
            'data': None
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class AssessmentResultViewSet(ViewSet):
    #permission_classes = [IsAuthenticated, SaaSAccessPermissionAssessment]
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_queryset():
        return AssessmentResult.objects.all()
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(AssessmentResult, pk=pk)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = AssessmentResultSerializer(queryset, many=True)
        response = {
            'status': 'success',
            'message': 'Assessment results list',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = AssessmentResultSerializer(instance)
        response = {
            'status': 'success',
            'message': 'Assessment result details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = AssessmentResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Assessment result created',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'error',
            'message': 'Invalid data',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = AssessmentResultSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Assessment result updated',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'error',
            'message': 'Invalid data',
            'data': serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'success',
            'message': 'Assessment result deleted',
            'data': None
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)


class AssessmentTypeViewSet(viewsets.ModelViewSet):
    queryset = AssessmentType.objects.all()
    serializer_class = AssessmentTypeSerializer
    permission_classes = [IsAuthenticated]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        org_id = self.request.query_params.get('org_id')
        if org_id:
            org = Org.objects.get(id=org_id)
            context['org'] = org
        return context

    @action(detail=True, methods=['post'])
    def map_questions(self, request, pk=None):
        assessment = self.get_object()
        org_id = request.data.get('org_id')
        org = Org.objects.get(id=org_id)

        serializer = self.get_serializer(assessment, data=request.data, partial=True, context={'org': org})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class AssessmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Access the sub-org from the Account model
        user_account = request.user.userprofile.account
        user_suborg = user_account.suborg  # Assuming sub-org is in Account model
        assessments = AssessmentType.objects.filter(suborg=user_suborg)
        serializer = AssessmentTypeSerializer(assessments, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Access the sub-org from the Account model
        user_account = request.user.userprofile.account
        user_suborg = user_account.suborg  # Assuming sub-org is in Account model
        data = request.data.copy()
        data['suborg'] = user_suborg.id  # Force setting suborg to user's suborg
        serializer = AssessmentTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, suborg):
        try:
            return AssessmentType.objects.get(pk=pk, suborg=suborg)
        except AssessmentType.DoesNotExist:
            return None

    def put(self, request, pk):
        # Access the sub-org from the Account model
        user_account = request.user.userprofile.account
        user_suborg = user_account.suborg  # Assuming sub-org is in Account model
        assessment = self.get_object(pk, user_suborg)

        if assessment is None:
            return Response({"error": "Assessment not found or you don't have access to edit it."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = AssessmentTypeSerializer(assessment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        