from django.urls import path, include
from .views import (
    ResourceListAPIView, ResourceCreateAPIView, ResourceRetrieveAPIView, ResourceUpdateAPIView,
    ResourceDestroyAPIView, TextResourceViewSet)
from rest_framework.routers import DefaultRouter    

router = DefaultRouter()
router.register(r'text-resources', TextResourceViewSet, basename='textresource')

urlpatterns = [
    path('resources/', ResourceListAPIView.as_view(), name='resource-list'),
    path('resources/create/', ResourceCreateAPIView.as_view(), name='resource-create'),
    path('resources/<int:pk>/', ResourceRetrieveAPIView.as_view(), name='resource-detail'),
    path('resources/<int:pk>/update/', ResourceUpdateAPIView.as_view(), name='resource-update'),
    path('resources/<int:pk>/delete/', ResourceDestroyAPIView.as_view(), name='resource-delete'),
    path('', include(router.urls)),


]