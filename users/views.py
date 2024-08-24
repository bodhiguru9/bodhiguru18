from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.permissions import IsAuthenticated

from users.serializers import UsersListSerializer, UsersSerializer
from users.serializers import UserCreateSerializer, UserRightSerializer
from users.serializers import UserSubOrgSerializer, UserMappingSerializer
from users.serializers import UserRightsMappingSerializer, UserRightsMappingListSerializer
from users.models import UserSubOrgs, UserMapping, UserRights, UserRightsMapping
from accounts.models import Account

class UsersViewSet(LoggingMixin, ViewSet):
    permission_classes  = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Account, pk=pk)
    
    @staticmethod
    def get_queryset():
        return Account.objects.all()
    
    def create(self, request):
        if request.user.user_role not in ['admin', 'super_admin']:
            response = {
                'status': "failed",
                'message': "You are not authorized to view this page",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
        request_data  = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'user_role': request.data.get('user_role', None),
            'role': request.data.get('role', None),
        }
        
        request_data['org'] = request.user.org.id if request.user.org else None
        
        serializer = UserCreateSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': "success",
                'message': "User created successfully",
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': "failed",
            'message': "User creation failed",
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        user_role = request.user.user_role
        if user_role not in ['admin', 'super_admin']:
            response = {
                'status': "failed",
                'message': "You are not authorized to view this page",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.get_queryset()
        if user_role.lower() == 'super_admin':
            queryset = queryset.filter(org=request.user.org)
        elif user_role.lower() == 'admin':
            queryset = queryset.filter(role__suborg=request.user.role.suborg)
        serializer = UsersListSerializer(queryset, many=True)
        response = {
            'status': "success",
            'message': "List of users",
            'data': serializer.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        if request.user.user_role not in ['admin', 'super_admin']:
            response = {
                'status': "failed",
                'message': "You are not authorized to view this page",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
        user = self.get_object(pk)
        serializer = UsersListSerializer(user)
        response = {
            'status': "success",
            'message': "User details",
            'data': serializer.data,
        }
        
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if request.user.user_role not in ['admin', 'super_admin']:
            response = {
                'status': "failed",
                'message': "You are not authorized to view this page",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
        user = self.get_object(pk)
        
        request_data  = {
            'first_name': request.data.get('first_name', user.first_name),
            'last_name': request.data.get('last_name', user.last_name),
            'email': request.data.get('email', user.email),
            'username': request.data.get('username', user.username),
            'user_role': request.data.get('user_role', user.user_role),
            'is_email_confirmed': request.data.get('is_email_confirmed', user.is_email_confirmed),
            'role': request.data.get('role', user.role.id if user.role else None),
            'org': request.data.get('org', user.org.id if user.org else None),
            'active': request.data.get('active', user.is_active),
        }
        
        serializer = UsersSerializer(user, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': "success",
                'message': "User updated successfully",
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': "failed",
            'message': "User update failed",
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if request.user.user_role not in ['admin', 'super_admin']:
            response = {
                'status': "failed",
                'message': "You are not authorized to view this page",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        
        user = self.get_object(pk)
        user.delete()
        response = {
            'status': "success",
            'message': "User deleted successfully",
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class UserSubOrgViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(UserSubOrgs, pk=pk)
    
    @staticmethod
    def get_queryset():
        return UserSubOrgs.objects.all()
    
    def create(self, request):
        request_data  = {
            'user': request.data.get('user', None),
            'suborg': request.data.get('suborg', None),
        }
        
        try:
            instance = UserSubOrgs.objects.get(user=request_data['user'], suborg=request_data['suborg'])
        except UserSubOrgs.DoesNotExist:
            serializer = UserSubOrgSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': "success",
                    'message': "User sub org created successfully",
                    'data': serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        if instance:
            response = {
                'status': "failed",
                'message': "User suborg mapping already exists",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'status': "failed",
            'message': "User sub org creation failed",
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UserMappingViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(UserMapping, pk=pk)
    
    @staticmethod
    def get_queryset():
        return UserMapping.objects.all()
    
    def create(self, request):
        request_data  = {
            'admin': request.data.get('admin', None),
            'user': request.data.get('user', None),
        }
        
        try:
            instance = UserMapping.objects.get(admin=request_data['admin'], user=request_data['user'])
        except UserMapping.DoesNotExist:
            serializer = UserMappingSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': "success",
                    'message': "User mapping created successfully",
                    'data': serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
        if instance:
            response = {
                'status': "failed",
                'message': "User mapping already exists",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'status': "failed",
            'message': "User mapping creation failed",
            'data': serializer.errors,
        }
        return Response(response, status=stat.HTTP_400_BAD_REQUEST)

class UserRightViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(UserRights, pk=pk)
    
    @staticmethod
    def get_queryset():
        return UserRights.objects.all()
    
    def list(self, request):
        serializer = UserRightSerializer(self.get_queryset(), many=True)
        response = {
            'status': "success",
            'message': "List of user rights",
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        user_right = self.get_object(pk)
        serializer = UserRightSerializer(user_right)
        response = {
            'status': "success",
            'message': "User right details",
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        request_data = {
            'name': request.data.get('name', None),
        }
        
        serializer = UserRightSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': "success",
                'message': "User right created successfully",
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'status': "failed",
            'message': "User right creation failed",
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        user_right = self.get_object(pk)
        request_data = {
            'name': request.data.get('name', user_right.name),
        }
        
        serializer = UserRightSerializer(user_right, data=request_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': "success",
                'message': "User right updated successfully",
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': "failed",
            'message': "User right update failed",
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user_right = self.get_object(pk)
        user_right.delete()
        response = {
            'status': "success",
            'message': "User right deleted successfully",
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class UserRightsMappingViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(UserRightsMapping, pk=pk)
    
    @staticmethod
    def get_queryset():
        return UserRightsMapping.objects.all()
    
    def list(self, request):
        user_id = request.query_params.get('user', None)
        
        rights = self.get_queryset().filter(user=user_id)
        serializer = UserRightsMappingListSerializer(rights, many=True)
        response = {
            'status': "success",
            'message': "List of user right mappings",
            'data': serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_id = request.data.get('user')
        right_id = request.data.get('right')

        if user_id is None or right_id is None:
            response = {
                'status': 'failed',
                'message': 'User ID and Right ID are required fields.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = UserRightsMapping.objects.get(user__id=user_id, right__id=right_id)
            response = {
                'status': 'failed',
                'message': 'User right mapping already exists',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except UserRightsMapping.DoesNotExist:
            request_data = {
                'user': user_id,
                'right': right_id,
            }
            serializer = UserRightsMappingSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'status': 'success',
                    'message': 'User right mapping created successfully',
                    'data': serializer.data,
                }
                return Response(response, status=status.HTTP_201_CREATED)
            response = {
                'status': 'failed',
                'message': 'User right mapping creation failed',
                'data': serializer.errors,
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        user_right_mapping = self.get_object(pk)
        request_data  = {
            'user': request.data.get('user', user_right_mapping.user.id),
            'right': request.data.get('right', user_right_mapping.right.id),
        }
        
        serializer = UserRightsMappingSerializer(user_right_mapping, data=request_data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': "success",
                'message': "User right mapping updated successfully",
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            'status': "failed",
            'message': "User right mapping update failed",
            'data': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user_right_mapping = self.get_object(pk)
        user_right_mapping.delete()
        response = {
            'status': "success",
            'message': "User right mapping deleted successfully",
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)
