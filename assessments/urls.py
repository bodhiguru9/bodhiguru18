from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import (AssessmentViewSet, AssessmentResultViewSet, AssessmentListCreateView,
                                AssessmentUpdateView, QuestionListCreateView, QuestionUpdateView, 
                                AssessmentResultCreateView, AssessmentResultListView,
                                UserAssessmentResultListView, AssessmentTypeListCreateView, AssessmentTypeListCreateView1, 
                                QuestionListView, AssessmentQuestionMappingView, SubmitAssessmentView)


router = DefaultRouter()

#router.register(r'assessments_question', AssessmentViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
    #path('assessments/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    #path('assessments/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),
    #path('assessments/', AssessmentTypeListCreateView.as_view(), name='assessment-list-create'),
    path('assessments1/', AssessmentTypeListCreateView1.as_view(), name='assessment1-lis1t-create1'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionUpdateView.as_view(), name='question-update'),
    #path('assessments_questions/', AssessmentListCreateView.as_view(), name='assessment-list-create'),
    #path('assessments_questions/<int:pk>/', AssessmentUpdateView.as_view(), name='assessment-update'),
    path('assessment-results/', AssessmentResultCreateView.as_view(), name='create-assessment-result'),
    path('assessment-results_list/', AssessmentResultListView.as_view(), name='assessment-results-list'),
    path('user-assessment-results/', UserAssessmentResultListView.as_view(), name='user-assessment-results'),
    path('submit-assessment/', SubmitAssessmentView.as_view(), name='submit-assessment'),
    path('questions_assessment/', QuestionListView.as_view(), name='question-list'),  # List questions based on org/suborg
    path('assessment/<int:assessment_id>/map-questions/', AssessmentQuestionMappingView.as_view(), name='map-questions'),  # Map questions to assessment




]

urlpatterns += router.urls