from django.urls import path, include

from rest_framework.routers import DefaultRouter

from learningcourse.views import LearningCourseViewSet, LearningCourseVideoViewSet
from learningcourse.views import LearningCourseDocumentViewSet

LearningCourseViewSetRouter = DefaultRouter()
LearningCourseVideoViewSetRouter = DefaultRouter()
LearningCourseDocumentViewSetRouter = DefaultRouter()

LearningCourseViewSetRouter.register("", LearningCourseViewSet, basename="LearningCourseViewSet")
LearningCourseVideoViewSetRouter.register("", LearningCourseVideoViewSet, basename="LearningCourseVideoViewSet")
LearningCourseDocumentViewSetRouter.register("", LearningCourseDocumentViewSet, basename="LearningCourseDocumentViewSet")

urlpatterns = [
    path("course/", include(LearningCourseViewSetRouter.urls)),
    path("video/", include(LearningCourseVideoViewSetRouter.urls)),
    path("document/", include(LearningCourseDocumentViewSetRouter.urls)),
]
