import csv
from io import StringIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrganizationReportSerializer
from django.db.models import Count
from orgss.models import Org
from zola.models import Item
from accounts.models import Account

class DailyReportAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Generate report data
        data = []
        organizations = Org.objects.all()

        for org in organizations:
            user_count = Account.objects.filter(organization=org).count()
            items_responded = Item.objects.filter(user__organization=org).count()

            data.append({
                'organization_name': org.name,
                'user_count': user_count,
                'items_responded': items_responded
            })

        # Convert data to CSV
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Organization Name', 'User Count', 'Items Responded'])
        for row in data:
            writer.writerow([row['organization_name'], row['user_count'], row['items_responded']])

        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="daily_report.csv"'
        return response