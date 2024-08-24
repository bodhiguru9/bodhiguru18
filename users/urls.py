from django.urls import path, include

from rest_framework.routers import DefaultRouter

from users.views import UsersViewSet, UserRightViewSet
from users.views import UserSubOrgViewSet, UserMappingViewSet, UserRightsMappingViewSet

UsersViewSetRouter = DefaultRouter()
UserSubOrgViewSetRouter = DefaultRouter()
UserMappingViewSetRouter = DefaultRouter()
UserRightViewSetRouter = DefaultRouter()
UserRightsMappingViewSetRouter = DefaultRouter()

UsersViewSetRouter.register("", UsersViewSet, basename='users')
UserRightViewSetRouter.register("", UserRightViewSet, basename='userrights')
UserSubOrgViewSetRouter.register("", UserSubOrgViewSet, basename='user_suborgs')
UserMappingViewSetRouter.register("", UserMappingViewSet, basename='user_mappings')
UserRightsMappingViewSetRouter.register("", UserRightsMappingViewSet, basename='userrights_mappings')

urlpatterns = [
    path("user/", include(UsersViewSetRouter.urls)),
    path("usersuborg/", include(UserSubOrgViewSetRouter.urls)),
    path("usermapping/", include(UserMappingViewSetRouter.urls)),
    path("userrights/", include(UserRightViewSetRouter.urls)),
    path("userightsmapping/", include(UserRightsMappingViewSetRouter.urls)),
]
