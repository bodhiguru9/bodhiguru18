from rest_framework import generics
from orgss.models import SubOrg
from org_analytics.serializers import SubOrgAnalyticsSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from accounts.models import Role

class IsAdminOrSubAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role.role_type in ['admin', 'sub-admin']

class SubOrgAnalyticsAPIView(generics.ListAPIView):
    serializer_class = SubOrgAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get_queryset(self):
        user = self.request.user
        return SubOrg.objects.filter(suborgrole__user=user)
