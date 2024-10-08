from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from series.models import Series, Seasons, SeasonLota, ItemSeason, AssessmentSeason
from assign.models import SeriesAssignUser
from series.serializers import (SeriesSerializer, SeasonSerializer, ItemSeasonSerializer,
                                ItemSeasonCreateUpdateSerializer, SeasonsListAssignSerializer,
                                SeasonLotaSerializer, SeasonLotaListSerializer, SeriesAdminSerializer,
                                SeasonAdminSerializer, AssessmentSeasonSerializer)

from rest_framework import viewsets
from .permissions import IsAdminOrSubAdmin

from zola.models import Item
from assessments.models import Assessment



class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            # Admins can see all series under their org
            return Series.objects.filter(sub_org__org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            # Sub-admins can only see series linked to their sub-org
            return Series.objects.filter(suborg=user_role.suborg)
        return Series.objects.none()


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            # Admins can see all seasons under series in their org
            return Seasons.objects.filter(series__sub_org__org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            # Sub-admins can only see seasons linked to series in their sub-org
            return Seasons.objects.filter(series__sub_org=user_role.suborg)
        return Seasons.objects.none()



class SeasonLotaViewSet(ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(SeasonLota, pk=pk)
    
    @staticmethod
    def get_queryset():
        return SeasonLota.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = SeasonLotaListSerializer(queryset, many=True)
        response = {
            "status": "success",
            "message": "SeasonLota list",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = SeasonLotaListSerializer(instance)
        response = {
            "status": "success",
            "message": "SeasonLota detail",
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = SeasonLotaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "SeasonLota created",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "status": "error",
            "message": "SeasonLota not created",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = SeasonLotaSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": "success",
                "message": "SeasonLota updated",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": "error",
            "message": "SeasonLota not updated",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            "status": "success",
            "message": "SeasonLota deleted",
        }
        return Response(response, status=status.HTTP_200_OK)

class ItemSeasonListCreateView(generics.ListCreateAPIView):
    queryset = ItemSeason.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ItemSeasonCreateUpdateSerializer
        return ItemSeasonSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            'status': 'success',
            'message': 'Item-Season mappings retrieved successfully',
            'data': response.data
        }
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'status': 'success',
            'message': 'Item-Season mapping created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)


class ItemSeasonRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ItemSeason.objects.all()
    serializer_class = ItemSeasonCreateUpdateSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'message': 'Item-Season mapping retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'status': 'success',
            'message': 'Item-Season mapping updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class SeriesAdminViewSet(viewsets.ModelViewSet):
    serializer_class = SeriesAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get_queryset(self):
        # Filter Series by the sub-org linked to the user
        role = getattr(self.request.user, 'role', None)
        if role:
            if role.role_type == 'admin':
                # Admin can see all series in their org's sub-orgs
                return Series.objects.filter(sub_org__org=role.sub_org.org)
            elif role.role_type == 'sub-admin':
                # Sub-admin can only see series in their sub-org
                return Series.objects.filter(sub_org=role.sub_org)
        return Series.objects.none()

class SeasonAdminViewSet(viewsets.ModelViewSet):
    serializer_class = SeasonAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get_queryset(self):
        # Filter Seasons by the series that belongs to the sub-org of the user
        role = getattr(self.request.user, 'role', None)
        if role:
            if role.role_type == 'admin':
                # Admin can see all seasons in their org's sub-org series
                return Season.objects.filter(series__sub_org__org=role.sub_org.org)
            elif role.role_type == 'sub-admin':
                # Sub-admin can only see seasons in their sub-org's series
                return Season.objects.filter(series__sub_org=role.sub_org)
        return Season.objects.none()

class ItemSeasonViewSet(viewsets.ModelViewSet):
    queryset = ItemSeason.objects.all()
    serializer_class = ItemSeasonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            # Admins can see all item-seasons linked to their org
            return ItemSeason.objects.filter(season__series__sub_org__org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            # Sub-admins can only see item-seasons linked to their sub-org
            return ItemSeason.objects.filter(season__series__sub_org=user_role.suborg)
        return ItemSeason.objects.none()        


class AssessmentSeasonCreateView(generics.CreateAPIView):
    queryset = AssessmentSeason.objects.all()
    serializer_class = AssessmentSeasonSerializer