from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import (AssessmentViewSet, AssessmentResultViewSet, AssessmentListCreateView,
                                AssessmentUpdateView, QuestionListCreateView, QuestionUpdateView)

from .views import AssessmentTypeViewSet, QuestionViewSet


router = DefaultRouter()
router.register(r'assessments', AssessmentTypeViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'assessments_question', AssessmentViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
    path('assessments/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('assessments/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionUpdateView.as_view(), name='question-update'),
    path('assessments_questions/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('assessments_questions/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),




]

urlpatterns += router.urls