from django.urls import path, include

from rest_framework.routers import DefaultRouter

from series.views import (SeriesViewSet, SeasonViewSet, SeasonLotaViewSet,
                            ItemSeasonListCreateView, ItemSeasonRetrieveUpdateView,
                            SeriesAdminViewSet, SeasonAdminViewSet, ItemSeasonViewSet,
                            AssessmentSeasonListCreateView, AssessmentSeasonDetailView
                            )



router = DefaultRouter()
router.register(r'series', SeriesViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'item-seasons', ItemSeasonViewSet, basename='itemseason')
#router.register(r'seriesadmin', SeriesViewSet, basename='series_admin')
#router.register(r'seasonsadmin', SeasonViewSet, basename='seasons_admin')

urlpatterns = [
    path('', include(router.urls)),
    path('itemseasons/', ItemSeasonListCreateView.as_view(), name='itemseason-list-create'),
    path('itemseasons/<int:id>/', ItemSeasonRetrieveUpdateView.as_view(), name='itemseason-retrieve-update'),
    path('assessment-seasons/', AssessmentSeasonListCreateView.as_view(), name='assessment-season-list-create'),
    path('assessment-seasons/<int:pk>/', AssessmentSeasonDetailView.as_view(), name='assessment-season-detail'),

    
]