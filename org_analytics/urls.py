from django.urls import path
from org_analytics.views import OrgAnalyticsView

urlpatterns = [
    
    # Org-level analytics
    path('analytics/org/<int:org_id>/', OrgAnalyticsView.as_view(), name='org-analytics'),
    # Sub-org-level analytics
    path('analytics/org/<int:org_id>/suborg/<int:suborg_id>/', OrgAnalyticsView.as_view(), name='suborg-analytics'),


]