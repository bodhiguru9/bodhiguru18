from django.urls import path
from .views import (
    ResourceListAPIView,
    ResourceCreateAPIView,
    ResourceRetrieveAPIView,
    ResourceUpdateAPIView,
    ResourceDestroyAPIView
)

urlpatterns = [
    path('resources/', ResourceListAPIView.as_view(), name='resource-list'),
    path('resources/create/', ResourceCreateAPIView.as_view(), name='resource-create'),
    path('resources/<int:pk>/', ResourceRetrieveAPIView.as_view(), name='resource-detail'),
    path('resources/<int:pk>/update/', ResourceUpdateAPIView.as_view(), name='resource-update'),
    path('resources/<int:pk>/delete/', ResourceDestroyAPIView.as_view(), name='resource-delete'),
]