from rest_framework.permissions import BasePermission

class IsAdminOrSubAdmin(BasePermission):
    """
    Custom permission to allow only admin or sub-admin users to view or edit.
    """
    def has_permission(self, request, view):
        user_role = getattr(request.user, 'role', None)
        if user_role:
            return user_role.role_type in ['admin', 'sub-admin']
        return False