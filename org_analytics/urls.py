from django.urls import path
from org_analytics.views import SubOrgAnalyticsAPIView

urlpatterns = [
    path('suborg-analytics/', SubOrgAnalyticsAPIView.as_view(), name='suborg-analytics'),
    # Add more URLs as needed
]