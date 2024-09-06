from rest_framework.permissions import BasePermission

class IsAdminOrSubAdmin(BasePermission):
    def has_permission(self, request, view):
        account = request.user  # Assuming user is logged in
        return account.role.role_type in ['admin', 'sub-admin']