from django.urls import path
from .views import PackageListView, PackageDetailView

urlpatterns = [
    path('packages/', PackageListView.as_view(), name='package-list'),
    path('packages/<int:pk>/', PackageDetailView.as_view(), name='package-detail'),
]