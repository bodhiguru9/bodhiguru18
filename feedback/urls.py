from django.urls import path
from .views import FeedbackView

urlpatterns = [
    path('submit/', FeedbackView.as_view(), name='submit-feedback'),
]