from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from accounts.models import Account, UserProfile
from orgss.models import Org
from django.db.models import Sum

class OrgReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orgs = Org.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="org_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Organization', 'Total Users', 'Active Users', 'Scenarios Attempted'])

        for org in orgs:
            total_users = Account.objects.filter(org=org).count()
            active_users = UserProfile.objects.filter(user__org=org, is_active=True, active=True).count()
            total_scenarios = UserProfile.objects.filter(user__org=org).aggregate(scenarios_sum=Sum('scenarios_attempted'))['scenarios_sum'] or 0

            writer.writerow([org.name, total_users, active_users, total_scenarios])

        return response


class OrgReportJsonView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        orgs = Org.objects.all()
        report_data = []

        for org in orgs:
            total_users = Account.objects.filter(org=org).count()
            active_users = UserProfile.objects.filter(user__org=org, is_active=True, active=True).count()
            total_scenarios = UserProfile.objects.filter(user__org=org).aggregate(scenarios_sum=Sum('scenarios_attempted'))['scenarios_sum'] or 0
            
            report_data.append({
                'organization': org.name,
                'total_users': total_users,
                'active_users': active_users,
                'scenarios_attempted': total_scenarios
            })

        return Response(report_data)        