from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from series.models import Series, Seasons, SeasonLota, ItemSeason
from assign.models import SeriesAssignUser
from series.serializers import SeriesSerializer, SeasonSerializer, ItemSeasonSerializer, ItemSeasonCreateUpdateSerializer

from series.serializers import SeasonsListAssignSerializer
from series.serializers import SeasonLotaSerializer, SeasonLotaListSerializer

from rest_framework import viewsets



class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer



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
