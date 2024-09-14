from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UpgradeViewSet
from . import views

router = DefaultRouter()
router.register(r'upgrade', UpgradeViewSet, basename='upgrade')

urlpatterns = [
    path('', include(router.urls)),
    path('payment_page/', views.payment_page, name='payment-page'),
    #path('payment_confirmation/', views.payment_confirmation, name='payment-confirmation'),
]