from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackageViewSet
from . import views

router = DefaultRouter()
router.register(r'packages', PackageViewSet, basename='packages')

urlpatterns = [
    path('', include(router.urls)),
    path('payment_page/', views.payment_page, name='payment-page'),
    path('payment_confirmation/', views.payment_confirmation, name='payment-confirmation'),
]