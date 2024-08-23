from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orgss.views import OrgViewSet, SubOrgViewSet, RoleViewSet

OrgViewSetRouter = DefaultRouter()
SubOrgViewSetRouter = DefaultRouter()
RoleViewSetRouter = DefaultRouter()

OrgViewSetRouter.register('', OrgViewSet, basename='org')
SubOrgViewSetRouter.register('', SubOrgViewSet, basename='suborg')
RoleViewSetRouter.register('', RoleViewSet, basename='role')

urlpatterns = [
    path('org/', include(OrgViewSetRouter.urls)),
    path('suborg/', include(SubOrgViewSetRouter.urls)),
    path('role/', include(RoleViewSetRouter.urls)),
]
