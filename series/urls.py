from django.urls import path, include

from rest_framework.routers import DefaultRouter

from series.views import (SeriesViewSet, SeasonViewSet, SeasonLotaViewSet,
                            ItemSeasonListCreateView, ItemSeasonRetrieveUpdateView,
                            SeriesAdminViewSet, SeasonAdminViewSet, ItemSeasonViewSet,
                            AssessmentSeasonCreateView, AssessmentSeasonView
                            )



router = DefaultRouter()
router.register(r'series', SeriesViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'item-seasons', ItemSeasonViewSet, basename='itemseason')


urlpatterns = [
    path('', include(router.urls)),
    path('itemseasons/', ItemSeasonListCreateView.as_view(), name='itemseason-list-create'),
    path('itemseasons/<int:id>/', ItemSeasonRetrieveUpdateView.as_view(), name='itemseason-retrieve-update'),
    path('assessment-season/', AssessmentSeasonCreateView.as_view(), name='assessment-season-create'),
    path('season_assessment/', AssessmentSeasonView.as_view(), name='assessment-season'),
    path('assessments/<int:assessment_id>/map-season/', AssessmentSeasonView.as_view(), name='map-season'),
    
]