from django.urls import path, include

from rest_framework.routers import DefaultRouter

from series.views import SeriesViewSet, SeasonsViewSet, SeasonLotaViewSet

SeriesViewSetRouter = DefaultRouter()
SeasonsViewSetRouter = DefaultRouter()
SeasonLotaViewSetRouter = DefaultRouter()

SeriesViewSetRouter.register("", SeriesViewSet, basename="SeriesViewSet")
SeasonsViewSetRouter.register("", SeasonsViewSet, basename="SeasonsViewSet")
SeasonLotaViewSetRouter.register("", SeasonLotaViewSet, basename=" SeasonLotaViewSet")

urlpatterns = [
    path("series/", include(SeriesViewSetRouter.urls)),
    path("seasons/", include(SeasonsViewSetRouter.urls)),
    path("seasonlota/", include(SeasonLotaViewSetRouter.urls)),
]
