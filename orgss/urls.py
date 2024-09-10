from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orgss.views import OrgViewSet, SubOrgViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'orgs', OrgViewSet)
router.register(r'suborgs', SubOrgViewSet)
router.register(r'roles', RoleViewSet)
#router.register(r'orgsadmin', OrgAdminViewSet, basename='org-admin')
#router.register(r'suborgsadmin', SubOrgAdminViewSet, basename='suborg-admin')

urlpatterns = [
    path('', include(router.urls)),
]