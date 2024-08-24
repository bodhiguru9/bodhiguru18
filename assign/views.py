from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from assign.models import SeriesAssignUser, AssessmentProgress, ItemProgress

from assign.serializers import SeriesAssignUserSerializer, SeriesAssignUserListSerializer
from assign.serializers import AssessmentProgressSerializer, ItemProgressSerializer

from series.models import Seasons, AssessmentSeason, ItemSeason, Series

from orgss.models import Role
from accounts.models import Account

class SeriesAssignUserViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(SeriesAssignUser, pk=pk)
    
    @staticmethod
    def get_queryset():
        return SeriesAssignUser.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = SeriesAssignUserListSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "Series Assign User List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = SeriesAssignUserListSerializer(instance)
        response = {
            "status": "success",
            "message": "Series Assign User Detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = SeriesAssignUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Series Assign User Created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = SeriesAssignUserSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Series Assign User Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "Series Assign User Deleted"
        }
        return Response(response, status=status.HTTP_200_OK)

class AssessmentProgressViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(AssessmentProgress, pk=pk)
    
    @staticmethod
    def get_queryset():
        return AssessmentProgress.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = AssessmentProgressSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "Assessment Progress List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = AssessmentProgressSerializer(instance)
        response = {
            "status": "success",
            "message": "Assessment Progress Detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data = {
            'user': request.data.get('user', request.user.id),
            'assessment_season': request.data.get('assessment_season'),
            'is_completed': request.data.get('is_completed', True),
        }
        
        assessment_found = AssessmentSeason.objects.filter(
            id=request_data["assessment_season"],
            season__series__seriesassignuser__user_id=request_data["user"]
        ).exists()

        if not assessment_found:
            response = {
                'status': 'error',
                'message': 'This assessment is not assigned to you',
            }
            return Response(response, status=status.HTTP_200_OK)
        
        serializer = AssessmentProgressSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Assessment Progress Created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = AssessmentProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Assessment Progress Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "Assessment Progress Deleted"
        }
        return Response(response, status=status.HTTP_200_OK)

class ItemProgressViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(ItemProgress, pk=pk)
    
    @staticmethod
    def get_queryset():
        return ItemProgress.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = ItemProgressSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "Item Progress List",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = ItemProgressSerializer(instance)
        response = {
            "status": "success",
            "message": "Item Progress Detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data = {
            'user': request.data.get('user', request.user.id),
            'item_season': request.data.get('item_season'),
            'is_completed': request.data.get('is_completed', True),
        }
        
        item_found = ItemSeason.objects.filter(
            id=request_data["item_season"],
            season__series__seriesassignuser__user_id=request_data["user"]
        ).exists()

        if not item_found:
            response = {
                'status': 'error',
                'message': 'This item is not assigned to you',
            }
            return Response(response, status=status.HTTP_200_OK)
        
        serializer = ItemProgressSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Item Progress Created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = ItemProgressSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "Item Progress Updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "Item Progress Deleted"
        }
        return Response(response, status=status.HTTP_200_OK)

class ProgressCheckViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        series_id = request.query_params.get("series")
        if series_id is None:
            return Response({"status": "error", "message": "Series ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        series = get_object_or_404(Series, id=series_id)
        seasons = Seasons.objects.filter(series=series).annotate(assessments_count=Count('assessmentseason'), items_count=Count('itemseason'))
        seasons_progress = {}

        assessments_progress_qs = AssessmentProgress.objects.filter(assessment_season__season__series=series, user=request.user).values_list('assessment_season_id', flat=True)
        items_progress_qs = ItemProgress.objects.filter(item_season__season__series=series, user=request.user).values_list('item_season_id', flat=True)
        assessments_progress_set = set(assessments_progress_qs)
        items_progress_set = set(items_progress_qs)

        for season in seasons:
            assessments_progress = {str(a_id): "Completed" for a_id in assessments_progress_set if a_id in season.assessmentseason_set.values_list('id', flat=True)}
            items_progress = {str(i_id): "Completed" for i_id in items_progress_set if i_id in season.itemseason_set.values_list('id', flat=True)}

            total_items = season.assessments_count + season.items_count
            completed_items = len(assessments_progress) + len(items_progress)
            progress = {
                "assessments": assessments_progress,
                "items": items_progress,
                "progress": (completed_items / total_items) * 100 if total_items > 0 else 0
            }
            seasons_progress[season.name] = progress

        series_progress = sum(season["progress"] for season in seasons_progress.values()) / len(seasons) if seasons else 0
        seasons_progress["series_progress"] = series_progress
        
        series_instance = SeriesAssignUser.objects.get(series=series, user=request.user)
        series_instance.progress = series_progress
        if series_progress == 100:
            series_instance.is_completed = True
        series_instance.save()
        response = {
            "status": "success",
            "message": "Progress Check",
            "data": seasons_progress
        }
        return Response(response, status=status.HTTP_200_OK)

class AssignSeriesByRoleViewSet(ViewSet):
    def create(self, request):
        request_data = {
            'series_id': request.data.get('series_id'),
            'role_id': request.data.get('role_id'),
        }
        
        if not request.data.get('series_id'):
            return Response({"status": "error", "message": "Series ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('role_id'):
            return Response({"status": "error", "message": "Role ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        users = Account.objects.filter(role__id=request_data["role_id"])
        
        if users:
            for user in users:
                try:
                    SeriesAssignUser.objects.create(user=user, series_id=request_data["series_id"])
                except:
                    pass
            
            response = {
                "status": "success",
                "message": "Series Assigned to Role"
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": "No users found with this role"
        }
        return Response(response, status=status.HTTP_200_OK)
