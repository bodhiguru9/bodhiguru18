from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UpgradeViewSet, UpgradeViewSet1, UpgradeAssessmentViewSet
from . import views

router = DefaultRouter()
router.register(r'upgrade', UpgradeViewSet, basename='upgrade')
router.register(r'upgrade_package', UpgradeViewSet1, basename='upgrade_package')
router.register(r'assessments', UpgradeAssessmentViewSet, basename='assessment')

urlpatterns = [
    path('', include(router.urls)),
    #path('payment_page/', views.payment_page, name='payment-page'),
    #path('payment_confirmation/', views.payment_confirmation, name='payment-confirmation'),
]