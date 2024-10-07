from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import pagination
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import UserRightsMapping
#m SaaS.permissions import SaaSAccessPermissionAssessment
from assessments.models import Question, Option, AssessmentType
from assessments.models import Assessment, AssessmentResult
from assessments.serializers import QuestionSerializer, OptionSerializer, OptionListSerializer
from assessments.serializers import AssessmentSerializer, AssessmentResultSerializer
from assessments.serializers import AssessmentListSerializer

from datetime import datetime

import threading

from rest_framework import viewsets
from .models import AssessmentType
from .serializers import AssessmentTypeSerializer

class QuestionViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_queryset():
        return Question.objects.all()
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Question, pk=pk)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = QuestionSerializer(queryset, many=True)
        response = {
            'status': 'success',
            'message': 'Questions list',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = QuestionSerializer(instance)
        response = {
            'status': 'success',
            'message': 'Question details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Question created',
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
        serializer = QuestionSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Question updated',
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
            'message': 'Question deleted',
            'data': None
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class OptionViewSet(ViewSet):
    @staticmethod
    def get_queryset():
        return Option.objects.all()
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Option, pk=pk)
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = OptionListSerializer(queryset, many=True)
        response = {
            'status': 'success',
            'message': 'Options list',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = OptionListSerializer(instance)
        response = {
            'status': 'success',
            'message': 'Option details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Option created',
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
        serializer = OptionSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Option updated',
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
            'message': 'Option deleted',
            'data': None
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class AssessmentTypeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_queryset():
        return AssessmentType.objects.all()
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(AssessmentType, pk=pk)
    
    def list(self, request):
        queryset = self.get_queryset()
        user = request.user
        if user.user_role not in ['admin', 'super_admin']:
            repsonse = {
                'status': 'error',
                'message': 'Access denied',
                'data': None
            }
        else:
            queryset = queryset.filter(suborg=user.role.suborg)
        serializer = AssessmentTypeSerializer(queryset, many=True)
        response = {
            'status': 'success',
            'message': 'Assessment types list',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = AssessmentTypeSerializer(instance)
        response = {
            'status': 'success',
            'message': 'Assessment type details',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        if not request.user.role.suborg:
            response = {
                'status': 'error',
                'message': 'Access denied',
                'data': None
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        
        request_data = {
            'name': request.data.get('name'),
            'suborg': request.user.role.suborg.id,
            'passing_criteria': request.data.get('passing_criteria'),
            'positive_marks': request.data.get('positive_marks'),
            'negative_marks': request.data.get('negative_marks'),
            'time': request.data.get('time'),
            'trigger_point': request.data.get('trigger_point'),
            'refresher_days': request.data.get('refresher_days')
        }
        
        serializer = AssessmentTypeSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Assessment type created',
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
            'name': request.data.get('name', instance.name),
            'suborg': instance.suborg.id,
            'passing_criteria': request.data.get('passing_criteria', instance.passing_criteria),
            'positive_marks': request.data.get('positive_marks', instance.positive_marks),
            'negative_marks': request.data.get('negative_marks', instance.negative_marks),
            'time': request.data.get('time', instance.time),
            'trigger_point': request.data.get('trigger_point', instance.trigger_point),
            'refresher_days': request.data.get('refresher_days', instance.refresher_days)
        }
        serializer = AssessmentTypeSerializer(instance, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'success',
                'message': 'Assessment type updated',
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
            'message': 'Assessment type deleted',
            'data': None
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

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