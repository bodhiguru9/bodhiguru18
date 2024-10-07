from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import AssessmentViewSet, AssessmentResultViewSet

from .views import AssessmentTypeViewSet, QuestionViewSet


router = DefaultRouter()
router.register(r'assessments', AssessmentTypeViewSet)
router.register(r'questions', QuestionViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
]

urlpatterns += router.urls