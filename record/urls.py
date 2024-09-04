# record/urls.py

from django.urls import path
from .views import OrgReportAPIView, DownloadOrgReportCSV

urlpatterns = [
    path('report/', OrgReportAPIView.as_view(), name='org-report'),
    path('report/download/', DownloadOrgReportCSV.as_view(), name='download-org-report'),
]
