from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.models import Account, UserProfile
from individual_analytics.serializers import UserSerializer1, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class IsAdminOrSubAdmin:
    def has_permission(self, request, view):
        try:
            account = Account.objects.get(user=request.user)
            role = account.role.role_type
            return role in ['admin', 'sub_admin']
        except Account.DoesNotExist:
            return False

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer1
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get_queryset(self):
        user = self.request.user
        try:
            account = Account.objects.get(user=user)
            role = account.role.role_type
            if role in ['admin', 'sub_admin']:
                # Get all accounts in the same org and fetch related users
                accounts_in_org = Account.objects.filter(org=account.org)
                return Account.objects.filter(account__in=accounts_in_org)
            else:
                raise PermissionDenied("You do not have permission to view this data.")
        except Account.DoesNotExist:
            return Account.objects.none()

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        try:
            account = Account.objects.get(user=user)
            role = account.role.role_type
            if role in ['admin', 'sub_admin']:
                # Get all accounts in the same org and fetch related users
                accounts_in_org = Account.objects.filter(org=account.org)
                return User.objects.filter(account__in=accounts_in_org)
            else:
                raise PermissionDenied("You do not have permission to view this data.")
        except Account.DoesNotExist:
            return User.objects.none()