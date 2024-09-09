from django.urls import path, include

from rest_framework.routers import DefaultRouter

from series.views import (SeriesViewSet, SeasonViewSet, SeasonLotaViewSet,
                            ItemSeasonListCreateView, ItemSeasonRetrieveUpdateView)


router = DefaultRouter()
router.register(r'series', SeriesViewSet)
router.register(r'seasons', SeasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('itemseasons/', ItemSeasonListCreateView.as_view(), name='itemseason-list-create'),
    path('itemseasons/<int:id>/', ItemSeasonRetrieveUpdateView.as_view(), name='itemseason-retrieve-update'),
]