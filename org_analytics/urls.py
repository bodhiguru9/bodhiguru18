from django.urls import path
from org_analytics.views import OrgAnalyticsView

urlpatterns = [
    path('analytics/', OrgAnalyticsView.as_view(), name='org-analytics'),
]