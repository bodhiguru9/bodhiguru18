from rest_framework import permissions
from .models import Account
from orgss.models import Org, SubOrg1

class IsAdminOrSubAdminOfOrg(permissions.BasePermission):
    """
    Custom permission to only allow admins or sub-admins of an organization/sub-organization to view or edit.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Get the user's account and check if they are an admin or sub-admin
        try:
            account = Account.objects.get(email=request.user.email)
            org = account.org
            sub_org = account.sub_org

            # Check if the user is an admin or sub-admin for their org or sub-org
            if account.role.role_type in ['admin', 'sub-admin']:
                return True
        except Account.DoesNotExist:
            return False

        return False

    def has_permission1(self, request, view):
        # Assuming you have a field is_admin on the user model
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        # Allow access only if the user is an admin of the org/sub-org
        return obj.org == request.user.org or obj.sub_org == request.user.sub_org    
