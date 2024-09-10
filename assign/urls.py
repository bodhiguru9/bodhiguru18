from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assign.views import (AssessmentProgressViewSet, ItemProgressViewSet,
                            AssignSeriesUserViewSet, SeriesAssignUserViewSet, ProgressCheckViewSet)

from assign.views import AssignSeriesByRoleViewSet

SeriesAssignUserViewSetRouter = DefaultRouter()
AssessmentProgressViewSetRouter = DefaultRouter()
ItemProgressViewSetRouter = DefaultRouter()
ProgressCheckViewSetRouter = DefaultRouter()
AssignSeriesByRoleViewSetRouter = DefaultRouter()

SeriesAssignUserViewSetRouter.register("", SeriesAssignUserViewSet, basename="series-assign-user")
AssessmentProgressViewSetRouter.register("", AssessmentProgressViewSet, basename="assessment-progress")
ItemProgressViewSetRouter.register("", ItemProgressViewSet, basename="item-progress")
ProgressCheckViewSetRouter.register("", ProgressCheckViewSet, basename="progress-check")
AssignSeriesByRoleViewSetRouter.register("", AssignSeriesByRoleViewSet, basename="assign-series-by-role")

router = DefaultRouter()
router.register(r'assign', AssignSeriesUserViewSet, basename='assign')

urlpatterns = [
    path("series/", include(SeriesAssignUserViewSetRouter.urls)),
    path("assessmentprogress/", include(AssessmentProgressViewSetRouter.urls)),
    path("itemprogress/", include(ItemProgressViewSetRouter.urls)),
    path("progresscheck/", include(ProgressCheckViewSetRouter.urls)),
    path("assignseriesbyrole/", include(AssignSeriesByRoleViewSetRouter.urls)),
    path('', include(router.urls)),
]
