from django.urls import path, include

from rest_framework.routers import DefaultRouter

from series.views import SeriesViewSet, SeasonViewSet, SeasonLotaViewSet


router = DefaultRouter()
router.register(r'series', SeriesViewSet)
router.register(r'seasons', SeasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]