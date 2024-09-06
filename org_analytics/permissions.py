from rest_framework.permissions import BasePermission
from accounts.models import Account

class IsAdminOrSubAdmin(BasePermission):
    def has_permission(self, request, view):
        account = Account.objects.filter(email=request.user.email).first()
        return account and account.role.role_type in ['admin', 'sub-admin']