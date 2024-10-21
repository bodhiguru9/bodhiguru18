from rest_framework.permissions import BasePermission

class IsAdminOrSubAdmin(BasePermission):
    """
    Allows access only to admins or sub-admins.
    """

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)
        return role and role.role_type in ['admin', 'sub-admin']

    def has_permission1(self, request, view):
        user_role = getattr(request.user, 'role', None)
        if user_role:
            return user_role.role_type in ['admin', 'sub-admin']
        return False        


class IsAdminOrSubAdmin1(BasePermission):
    """
    Custom permission to allow access to users with is_admin=True or with 'admin'/'sub-admin' roles.
    """

    def has_permission(self, request, view):
        user = request.user
        # If user is admin, allow access
        if user.is_admin:
            return True
        
        # If user has a role and it is either 'admin' or 'sub-admin', allow access
        user_role = getattr(user, 'role', None)
        if user_role and user_role.role_type in ['admin', 'sub-admin']:
            return True
        
        # Deny access if none of the above conditions are met
        return False