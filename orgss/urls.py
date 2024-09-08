from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orgss.views import OrgViewSet, SubOrgViewSet, RoleViewSet


router = DefaultRouter()
router.register(r'org', OrgViewSet)
router.register(r'suborg', SubOrgViewSet)
router.register(r'role', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]