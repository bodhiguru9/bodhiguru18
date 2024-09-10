from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orgss.views import OrgViewSet, SubOrgViewSet, RoleViewSet, OrgAdminViewSet, SubOrgAdminViewSet

router = DefaultRouter()
router.register(r'org', OrgViewSet)
router.register(r'suborg', SubOrgViewSet)
router.register(r'role', RoleViewSet)
router.register(r'orgsadmin', OrgAdminViewSet, basename='org-admin')
router.register(r'suborgsadmin', SubOrgAdminViewSet, basename='suborg-admin')

urlpatterns = [
    path('', include(router.urls)),
]