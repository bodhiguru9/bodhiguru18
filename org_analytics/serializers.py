from rest_framework import serializers

from accounts.models import UserProfile, Account
from orgss.models import Org, SubOrg1, Role1



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'scenarios_attempted', 'user']  

class UserAnalyticsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_scenarios_attempted = serializers.IntegerField()
    users = serializers.ListField()

class UserScenarioDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')  # Reference 'user.email' for the email

    class Meta:
        model = UserProfile
        fields = ['email', 'scenarios_attempted']