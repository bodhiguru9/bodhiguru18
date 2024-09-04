from django.urls import path
from .views import DailyReportAPIView

urlpatterns = [
    path('daily-report/', DailyReportAPIView.as_view(), name='daily-report'),
]