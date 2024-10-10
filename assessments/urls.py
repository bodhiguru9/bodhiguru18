from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import (AssessmentViewSet, AssessmentResultViewSet, AssessmentListCreateView,
                                AssessmentUpdateView, QuestionListCreateView, QuestionUpdateView, 
                                AssessmentResultCreateView, AssessmentResultListView,
                                UserAssessmentResultListView, AssessmentTypeListCreateView)

from .views import QuestionViewSet


router = DefaultRouter()
#router.register(r'assessments', AssessmentTypeViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'assessments_question', AssessmentViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
    #path('assessments/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    #path('assessments/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),
    path('assessments/', AssessmentTypeListCreateView.as_view(), name='assessment-list-create'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionUpdateView.as_view(), name='question-update'),
    path('assessments_questions/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    path('assessments_questions/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),
    path('assessment-results/', AssessmentResultCreateView.as_view(), name='create-assessment-result'),
    path('assessment-results_list/', AssessmentResultListView.as_view(), name='assessment-results-list'),
    path('user-assessment-results/', UserAssessmentResultListView.as_view(), name='user-assessment-results'),




]

urlpatterns += router.urls