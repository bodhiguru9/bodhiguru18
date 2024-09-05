from rest_framework.permissions import BasePermission
from accounts.models import Account

class IsAdminOrSubAdmin(BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Get the admin/sub_admin's account
        try:
            account = Account.objects.get(email=request.user.email)
        except Account.DoesNotExist:
            return False

        # Check if the user's role is admin or sub_admin
        return account.role.role_type in ['admin', 'sub_admin']

    def has_object_permission(self, request, view, obj):
        # Ensure the user is part of the same organization
        try:
            account = Account.objects.get(email=request.user.email)
        except Account.DoesNotExist:
            return False
        
        return obj.org == account.org