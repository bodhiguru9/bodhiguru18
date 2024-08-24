from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import QuestionViewSet, OptionViewSet, AssessmentTypeViewSet
from assessments.views import AssessmentViewSet, AssessmentResultViewSet

QuestionViewSetRouter = DefaultRouter()
OptionViewSetRouter = DefaultRouter()
AssessmentTypeViewSetRouter = DefaultRouter()
AssessmentViewSetRouter = DefaultRouter()
AssessmentResultViewSetRouter = DefaultRouter()

QuestionViewSetRouter.register('', QuestionViewSet, basename='question')
OptionViewSetRouter.register('', OptionViewSet, basename='option')
AssessmentTypeViewSetRouter.register('', AssessmentTypeViewSet, basename='assessmenttype')
AssessmentViewSetRouter.register('', AssessmentViewSet, basename='assessment')
AssessmentResultViewSetRouter.register('', AssessmentResultViewSet, basename='assessmentresult')

urlpatterns = [
    path('question/', include(QuestionViewSetRouter.urls)),
    path('option/', include(OptionViewSetRouter.urls)),
    path('assessmenttype/', include(AssessmentTypeViewSetRouter.urls)),
    path('assessment/', include(AssessmentViewSetRouter.urls)),
    path('assessmentresult/', include(AssessmentResultViewSetRouter.urls)),
]
