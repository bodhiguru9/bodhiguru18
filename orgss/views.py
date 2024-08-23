from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from orgss.models import Org, SubOrg, Role
from orgss.serilaizers import OrgSerializer, OrgListSerializer
from orgss.serilaizers import SubOrgSerializer, SubOrgListSerializer
from orgss.serilaizers import RoleSerializer, RoleListSerializer

class OrgViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Org, id=pk)

    @staticmethod
    def get_queryset():
        return Org.objects.all()

    def list(self, request):
        serialized_data = OrgListSerializer(self.get_queryset(), many=True).data
        response = {
            'status': 'Success',
            'message': "Orgs has been successfully retrieved.",
            'data': serialized_data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, **kwargs):
        pk = kwargs.pop('pk')
        response = {
            'status': 'Success',
            'message': 'Org has been successfully retrieved.',
            'data': OrgListSerializer(self.get_object(pk)).data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        request_data = self.request.data
        data = {
            'name': request_data.get('name'),
            'description': request_data.get('description'),
            'industry': request_data.get('industry'),
        }
        
        serializer = OrgSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'data': serializer.data,
                'message': 'Org was successfully created.'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'Failed',
            'message': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        request_data = self.request.data
        
        data = {
            'name': request_data.get('name', instance.name),
            'description': request_data.get('description', instance.description),
            'industry': request_data.get('industry', instance.industry.id),
        }
        
        serializer = OrgSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'data': serializer.data,
                'message': 'Org was successfully updated.'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'Failed',
            'message': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        instance.delete()

        response = {
            'data': '',
            'message': "Successfully deleted Org"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class SubOrgViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(SubOrg, id=pk)

    @staticmethod
    def get_queryset():
        return SubOrg.objects.all()

    def list(self, request):
        queryset = self.get_queryset().filter(org=request.user.org)
        serialized_data = SubOrgListSerializer(queryset, many=True).data
        response = {
            'status': 'Success',
            'message': "SubOrgs has been successfully retrieved.",
            'data': serialized_data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, pk=None):
        response = {
            'status': 'Success',
            'message': 'SubOrg has been successfully retrieved.',
            'data': SubOrgListSerializer(self.get_object(pk)).data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        request_data = self.request.data
        data = {
            'name': request_data.get('name'),
            'description': request_data.get('description'),
            'org': request_data.get('org'),
        }
        
        serializer = SubOrgSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'data': serializer.data,
                'message': 'SubOrg was successfully created.'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'Failed',
            'message': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        request_data = self.request.data
        
        data = {
            'name': request_data.get('name', instance.name),
            'description': request_data.get('description', instance.description),
            'org': request_data.get('org', instance.org.id),
        }
        
        serializer = SubOrgSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'data': serializer.data,
                'message': 'SubOrg was successfully updated.'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'Failed',
            'message': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        instance.delete()

        response = {
            'data': '',
            'message': "Successfully deleted SubOrg"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class RoleViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Role, id=pk)

    @staticmethod
    def get_queryset():
        return Role.objects.all()

    def list(self, request):
        roles_data = self.get_queryset().filter(suborg__org=request.user.org)
        serialized_data = RoleListSerializer(roles_data, many=True).data
        response = {
            'status': 'Success',
            'message': "Roles has been successfully retrieved.",
            'data': serialized_data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, pk=None):
        response = {
            'status': 'Success',
            'message': 'Role has been successfully retrieved.',
            'data': RoleListSerializer(self.get_object(pk)).data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    
    def create(self, request):
        request_data = self.request.data
        data = {
            'name': request_data.get('name'),
            'suborg': request_data.get('suborg'),
        }
        
        serializer = RoleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'data': serializer.data,
                'message': 'Role was successfully created.'
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': 'Failed',
            'message': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        request_data = self.request.data
        
        data = {
            'name': request_data.get('name', instance.name),
            'suborg': request_data.get('suborg', instance.suborg.id),
        }
        
        serializer = RoleSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 'Success',
                'data': serializer.data,
                'message': 'Role was successfully updated.'
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': 'Failed',
            'message': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, **kwargs):
        instance = self.get_object(kwargs.pop('pk'))
        instance.delete()

        response = {
            'status': 'Success',
            'message': "Successfully deleted Role"
        }
        return Response(response, status=status.HTTP_200_OK)
