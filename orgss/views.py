from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from orgss.models import Org, SubOrg1, Role1
from orgss.serializers import OrgSerializer, OrgListSerializer
from orgss.serializers import SubOrgSerializer, SubOrgListSerializer
from orgss.serializers import RoleSerializer, RoleListSerializer

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