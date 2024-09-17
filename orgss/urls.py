from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orgss.views import OrgViewSet, SubOrgViewSet, RoleViewSet, OrgAdminViewSet, WeightageViewSet

router = DefaultRouter()
router.register(r'orgs', OrgViewSet)
router.register(r'suborgs', SubOrgViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'view', OrgAdminViewSet, basename='org-admin')
router.register(r'weightages', WeightageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
]