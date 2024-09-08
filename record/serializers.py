from rest_framework import serializers
from orgss.models import Org
from accounts.models import Account, UserProfile

class OrgReportSerializer(serializers.ModelSerializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    scenarios_attempted = serializers.IntegerField()

    class Meta:
        model = Org
        fields = ['name', 'total_users', 'active_users', 'scenarios_attempted']   