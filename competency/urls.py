from django.urls import path, include

from rest_framework.routers import DefaultRouter

from competency.views import CompetencyViewSet

CompetencyViewSetRouter = DefaultRouter()

CompetencyViewSetRouter.register('', CompetencyViewSet, basename='competency')

urlpatterns = [
    path('', include(CompetencyViewSetRouter.urls)),
]
