from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from zola.views import ItemList, item_result, item_rec
from zola.views import ItemViewSet, ItemHandleViewSet
from zola.views import ItemProcessingViewSet, ItemAnalysticsViewSet
from zola.views import (LeaderBoardViewSet, CompetencyBoardViewSet, CompetencyAttemptAnalyticsViewSet,
                        SubmitScoreView, CheckLevelProgressionView, ItemSearchView, ItemLibraryAPIView, LeaderboardPercentileAPIView)

ItemViewSetRouter = DefaultRouter()
ItemHandleViewSetRouter = DefaultRouter()
ItemProcessingViewSetRouter = DefaultRouter()
ItemAnalysticsViewSetRouter = DefaultRouter()
LeaderBoardViewSetRouter = DefaultRouter()
CompetencyBoardViewSetRouter = DefaultRouter()
CompetencyAttemptAnalyticsViewSetRouter = DefaultRouter()

ItemViewSetRouter.register('', ItemViewSet, basename='item')
ItemHandleViewSetRouter.register('', ItemHandleViewSet, basename='itemhandle')
ItemProcessingViewSetRouter.register('', ItemProcessingViewSet, basename='itemprocessing')
ItemAnalysticsViewSetRouter.register('', ItemAnalysticsViewSet, basename='itemanalystics')
LeaderBoardViewSetRouter.register('', LeaderBoardViewSet, basename='leaderboard')
CompetencyBoardViewSetRouter.register('', CompetencyBoardViewSet, basename='competencyboard')
CompetencyAttemptAnalyticsViewSetRouter.register('', CompetencyAttemptAnalyticsViewSet, basename='lastitemattemptedanalytics')


urlpatterns = [
    re_path(r'^api/item_results/(?P<pk>[0-9]+)$', item_result),
    re_path(r'^api/item_rec/(?P<pk>[0-9]+)$', item_rec),
    path('item/', include(ItemViewSetRouter.urls)),
    path('itemhandle/', include(ItemHandleViewSetRouter.urls)),
    path('itemprocessing/', include(ItemProcessingViewSetRouter.urls)),
    path('itemanalystics/', include(ItemAnalysticsViewSetRouter.urls)),
    path('itemli/', ItemList.as_view(), name="Item_List"),
    path('leaderboard/', include(LeaderBoardViewSetRouter.urls)),
    path('competency/', include(CompetencyBoardViewSetRouter.urls)),
    path('lastitemanalytics/', include(CompetencyAttemptAnalyticsViewSetRouter.urls)),
    path('submit-score/', SubmitScoreView.as_view(), name='submit-score'),
    path('check-level-progression/', CheckLevelProgressionView.as_view(), name='check-level-progression'),
    path('items/search/', ItemSearchView.as_view(), name='item-search'),
    path('item_library/', ItemLibraryAPIView.as_view(), name='item-list'),
    path('leaderboardpercentile/', LeaderboardPercentileAPIView.as_view(), name='leaderboard'),

]