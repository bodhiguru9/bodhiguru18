from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import (AssessmentViewSet, AssessmentResultViewSet, AssessmentListCreateView,
                                AssessmentUpdateView)

from .views import AssessmentTypeViewSet, QuestionViewSet


router = DefaultRouter()
router.register(r'assessments', AssessmentTypeViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'assessments_question', AssessmentViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
    path('assessments/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('assessments/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),




]

urlpatterns += router.urls