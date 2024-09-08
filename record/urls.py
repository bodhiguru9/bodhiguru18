from django.urls import path
#from .views import OrgReportAPIView, DownloadOrgReportCSV
from .views import OrgReportView, OrgReportJsonView


urlpatterns = [
    # URL to download the CSV report
    path('org-report-csv/', OrgReportView.as_view(), name='org-report-csv'),

    # URL to get the report data as JSON
    path('org-report-json/', OrgReportJsonView.as_view(), name='org-report-json'),
]