from rest_framework.permissions import BasePermission

class IsAdminOrSubAdmin(BasePermission):
    """
    Allows access only to admins or sub-admins.
    """

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)
        return role and role.role_type in ['admin', 'sub-admin']