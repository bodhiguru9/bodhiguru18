# record/views.py

import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orgss.models import Org  # Assuming your orgss app is named 'orgss'
from accounts.models import Account, UserProfile
#from profiles.models import UserProfile  # Assuming profiles app has UserProfile model
from .serializers import OrgReportSerializer

class OrgReportAPIView(APIView):
    def get(self, request, format=None):
        report_data = []

        orgs = Org.objects.all()

        for org in orgs:
            users = Account.objects.filter(org=org)
            user_count = users.count()
            total_scenarios_attempted = 0

            for user in users:
                user_profile = UserProfile.objects.get(user=user)
                total_scenarios_attempted += user_profile.scenarios_attempted  # Adjust field name as necessary

            report_data.append({
                'org_name': org.name,
                'user_count': user_count,
                'total_scenarios_attempted': total_scenarios_attempted
            })

        serializer = OrgReportSerializer(report_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadOrgReportCSV(APIView):
    def get(self, request, format=None):
        # Create the HttpResponse object with CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="org_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Organization Name', 'Number of Users', 'Total Scenarios Attempted'])

        orgs = Org.objects.all()

        for org in orgs:
            users = Account.objects.filter(org=org)
            user_count = users.count()
            total_scenarios_attempted = 0

            for user in users:
                user_profile = UserProfile.objects.get(user=user)
                total_scenarios_attempted += user_profile.scenarios_attempted  # Adjust field name as necessary

            writer.writerow([org.name, user_count, total_scenarios_attempted])

        return response
