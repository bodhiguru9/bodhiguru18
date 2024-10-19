from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit Org and SubOrg.
    """
    def has_permission(self, request, view):
        # Assume that the request.user is linked to a Role through the Profile model or another method
        role = getattr(request.user, 'role', None)
        return bool(role and role.role_type == 'admin')

class IsSubAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow sub-admins to edit SubOrg they are linked to.
    """
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)
        return bool(role and role.role_type in ['admin', 'sub-admin'])
    
    def has_object_permission(self, request, view, obj):
        # Sub-admins can only edit their linked SubOrg, Admin can edit all.
        role = getattr(request.user, 'role', None)
        if role.role_type == 'admin':
            return True
        return obj == role.sub_org

class IsAdminOrSubAdmin(BasePermission):
    """
    Custom permission to only allow admin or sub-admin users to access the API.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.role.role_type in ['admin', 'sub-admin'])        