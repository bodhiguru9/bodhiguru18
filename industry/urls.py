from django.urls import path, include
from rest_framework.routers import DefaultRouter

from industry.views import IndustryViewSet

router =  DefaultRouter()
router.register('business', IndustryViewSet, basename='business')

urlpatterns = [
    path('', include(router.urls))
]
