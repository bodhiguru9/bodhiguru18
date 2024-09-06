from rest_framework import serializers
from accounts.models import UserProfile
from orgss.models import Org

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'scenarios_attempted',
                  'user_powerwords', 'user_weakwords', 'competency_score', 'current_level']

class OrgOverviewSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_scenarios_attempted = serializers.IntegerField()
    scenarios_per_user = serializers.DictField(child=serializers.IntegerField())
    leaderboard = serializers.ListField(child=serializers.DictField())