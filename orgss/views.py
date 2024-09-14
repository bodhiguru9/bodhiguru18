from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from orgss.models import Org, SubOrg1, Role1
from orgss.serializers import (OrgSerializer, OrgListSerializer, OrgAdminSerializer, SubOrgAdminSerializer,
                                SubOrgSerializer, SubOrgListSerializer, RoleSerializer, RoleListSerializer
                               )

from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly, IsSubAdminOrReadOnly

from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework import generics, permissions

from rest_framework.views import APIView

from accounts.models import Account

from rest_framework.parsers import MultiPartParser, FormParser


class OrgViewSet(viewsets.ModelViewSet):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]

class SubOrgViewSet(viewsets.ModelViewSet):
    queryset = SubOrg1.objects.all()
    serializer_class = SubOrgSerializer
    permission_classes = [IsAuthenticated]

    # Admin or sub-admin can only access sub-orgs linked to their org/sub-org
    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            return SubOrg1.objects.filter(org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            return SubOrg1.objects.filter(id=user_role.suborg.id)
        return SubOrg1.objects.none()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role1.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    # Admin or sub-admin can only access roles linked to their org/sub-org
    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            return Role1.objects.filter(suborg__org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            return Role1.objects.filter(suborg=user_role.suborg)
        return Role1.objects.none()
"""
class OrgAdminViewSet(viewsets.ModelViewSet):
    queryset = Org.objects.all()
    serializer_class = OrgAdminSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        # Only allow admins to see orgs they manage
        role = getattr(self.request.user, 'role', None)
        if role and role.role_type == 'admin':
            return Org.objects.all()
        return Org.objects.none()

class SubOrgAdminViewSet(viewsets.ModelViewSet):
    queryset = SubOrg1.objects.all()
    serializer_class = SubOrgAdminSerializer
    permission_classes = [IsSubAdminOrReadOnly]

    def get_queryset(self):
        # Admin can see all sub-orgs under their org, sub-admin only their own sub-org
        role = getattr(self.request.user, 'role', None)
        if role:
            if role.role_type == 'admin':
                return SubOrg1.objects.filter(org=role.suborg.org)
            elif role.role_type == 'sub-admin':
                return SubOrg1.objects.filter(id=role.suborg.id)
        return SubOrg1.objects.none()    
"""
class OrgAdminViewSet(viewsets.ModelViewSet):
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_email = self.request.user.email  # Assuming the user’s email is available in the request
        try:
            user_account = Account.objects.get(email=user_email)
            return Org.objects.filter(id=user_account.org.id)
        except Account.DoesNotExist:
            return Org.objects.none()

    def get_object(self):
        user_email = self.request.user.email
        try:
            user_account = Account.objects.get(email=user_email)
            return Org.objects.get(id=user_account.org.id)
        except (Account.DoesNotExist, Org.DoesNotExist):
            return None