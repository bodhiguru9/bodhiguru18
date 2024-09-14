from django.urls import path, include
from .views import PackageListView, PackageDetailView, PackageViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='packages')

urlpatterns = [
    path('packages/', PackageListView.as_view(), name='package-list'),
    path('packages/<int:pk>/', PackageDetailView.as_view(), name='package-detail'),
    path('', include(router.urls)),

]