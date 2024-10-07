from django.urls import path, include

from rest_framework.routers import DefaultRouter

from assessments.views import QuestionViewSet, OptionViewSet
from assessments.views import AssessmentViewSet, AssessmentResultViewSet

from .views import AssessmentTypeViewSet


router = DefaultRouter()
router.register(r'assessments', AssessmentTypeViewSet)


urlpatterns = [
    
    path('', include(router.urls)),
]

urlpatterns += router.urls