from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orgss.views import OrgViewSet, SubOrgViewSet, RoleViewSet, OrgAdminViewSet, WeightageViewSet, org_expiry_view

router = DefaultRouter()
#router.register(r'orgs', OrgViewSet)
#router.register(r'suborgs', SubOrgViewSet)
#router.register(r'roles', RoleViewSet)
router.register(r'orgs', OrgViewSet, basename='org')
router.register(r'suborgs', SubOrgViewSet, basename='suborg')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'view', OrgAdminViewSet, basename='org-admin')
router.register(r'weightages', WeightageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('org-expiry/', org_expiry_view, name='org-expiry'), 
    
]