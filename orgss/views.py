from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from orgss.models import Org, SubOrg1, Role1
from orgss.serializers import (OrgSerializer, OrgListSerializer, OrgAdminSerializer, SubOrgAdminSerializer,
                                SubOrgSerializer, SubOrgListSerializer, RoleSerializer, RoleListSerializer)

from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly, IsSubAdminOrReadOnly

from rest_framework import viewsets


class OrgViewSet(viewsets.ModelViewSet):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer

class SubOrgViewSet(viewsets.ModelViewSet):
    queryset = SubOrg1.objects.all()
    serializer_class = SubOrgSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role1.objects.all()
    serializer_class = RoleSerializer

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