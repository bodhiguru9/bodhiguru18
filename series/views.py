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
                                SeasonAdminSerializer, AssessmentSeasonSerializer, AssessmentSeasonSerializer1)

from rest_framework import viewsets
from .permissions import IsAdminOrSubAdmin, IsAdminOrSubAdmin1
from zola.models import Item
from assessments.models import Assessment
from orgss.models import SubOrg1



"""
class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        sub_orgs = []

        if user.is_admin:
            # Admin can see all series under their org
            sub_orgs = SubOrg1.objects.filter(org=user.org)
            return Series.objects.filter(sub_org__org=user.org)

        user_role = user.role  # This can return None if not set

        if user_role and user_role.role_type == 'admin':
            # Admins can see all series under their org
            sub_orgs = SubOrg1.objects.filter(org=user_role.suborg.org)
            return Series.objects.filter(sub_org__org=user_role.suborg.org)

        elif user_role and user_role.role_type == 'sub-admin':
            # Sub-admins can only see series linked to their sub-org
            sub_orgs = [user_role.suborg]
            return Series.objects.filter(sub_org=user_role.suborg)

        # Print the sub-orgs for debugging
        print("Sub-orgs available for the logged-in user:")
        for sub_org in sub_orgs:
            print(f"- {sub_org.name} (ID: {sub_org.id})")

        return Series.objects.none()  # No access for other roles

    def list(self, request, *args, **kwargs):
        # Override the list method to include additional context in the response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Get sub-orgs again for the response
        user = self.request.user
        sub_orgs = []

        if user.is_admin:
            sub_orgs = SubOrg1.objects.filter(org=user.org)
        elif user.role and user.role.role_type == 'admin':
            sub_orgs = SubOrg1.objects.filter(org=user.role.suborg.org)
        elif user.role and user.role.role_type == 'sub-admin':
            sub_orgs = [user.role.suborg]

        # Include the sub-orgs in the response
        return Response({
            'series': serializer.data,
            'sub_orgs': [{'id': sub_org.id, 'name': sub_org.name} for sub_org in sub_orgs]
        })

    def get_serializer_context(self):
        # Add the user to the context
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            # Admin can see all series under their org
            return Series.objects.filter(sub_org__org=user.org)
        
        user_role = user.role  # This can return None if not set
        
        if user_role and user_role.role_type == 'admin':
            # Admins can see all series under their org
            return Series.objects.filter(sub_org__org=user_role.suborg.org)
        
        elif user_role and user_role.role_type == 'sub-admin':
            # Sub-admins can only see series linked to their sub-org
            return Series.objects.filter(sub_org=user_role.suborg)
        
        return Series.objects.none()  # No access for other roles

    def get_serializer_context(self):
        # Add the user to the context
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context
"""

class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            # Admin can see all series under their org
            return Series.objects.filter(sub_org__org=user.org)
        
        user_role = user.role  # This can return None if not set
        
        if user_role and user_role.role_type == 'admin':
            # Admins can see all series under their org
            return Series.objects.filter(sub_org__org=user_role.suborg.org)
        
        elif user_role and user_role.role_type == 'sub-admin':
            # Sub-admins can only see series linked to their sub-org
            return Series.objects.filter(sub_org=user_role.suborg)
        
        return Series.objects.none()

    def get_serializer_context(self):
        # Add the user to the context
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_serializer(self, *args, **kwargs):
        # Explicitly pass the user to the serializer
        kwargs['user'] = self.request.user
        return super().get_serializer(*args, **kwargs)



class SeasonViewSet(viewsets.ModelViewSet):
    queryset = Seasons.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_role = getattr(user, 'role', None)

        if user.is_admin or (user_role and user_role.role_type == 'admin'):
            # Admins can see all seasons under series in their org
            return Seasons.objects.filter(series__sub_org__org=user.org)
        elif user_role and user_role.role_type == 'sub-admin':
            # Sub-admins can only see seasons linked to series in their sub-org
            return Seasons.objects.filter(series__sub_org=user.sub_org)
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
"""
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
"""

class ItemSeasonViewSet(viewsets.ModelViewSet):
    queryset = ItemSeason.objects.all()
    serializer_class = ItemSeasonSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin1]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            # If user has is_admin=True, allow access to all ItemSeason objects
            return ItemSeason.objects.all()
        
        user_role = getattr(user, 'role', None)
        
        if user_role:
            if user_role.role_type == 'admin':
                # Admins can see all item-seasons linked to their org
                return ItemSeason.objects.filter(season__series__sub_org__org=user_role.suborg.org)
            elif user_role.role_type == 'sub-admin':
                # Sub-admins can only see item-seasons linked to their sub-org
                return ItemSeason.objects.filter(season__series__sub_org=user_role.suborg)
        
        # If the user has no role or unauthorized role
        return ItemSeason.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        # Check if user has the correct permissions to create a mapping
        if not user.is_admin and not getattr(user, 'role', None):
            return Response({
                'status': 'failure',
                'message': 'You do not have permission to perform this action'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        # Check if user has the correct permissions to update a mapping
        if not user.is_admin and not getattr(user, 'role', None):
            return Response({
                'status': 'failure',
                'message': 'You do not have permission to perform this action'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)


class AssessmentSeasonCreateView(generics.CreateAPIView):
    queryset = AssessmentSeason.objects.all()
    serializer_class = AssessmentSeasonSerializer

class AssessmentSeasonView(generics.ListCreateAPIView):
    queryset = AssessmentSeason.objects.all()
    serializer_class = AssessmentSeasonSerializer1
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        sub_org = user.sub_org  # User's sub_org

        if sub_org:
            # Filter seasons based on the series that are mapped to the user's sub_org
            return Seasons.objects.filter(series__sub_org=sub_org)
        else:
            raise serializers.ValidationError("User is not associated with any sub-organization.")