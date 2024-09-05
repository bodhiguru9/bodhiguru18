from rest_framework import serializers
from accounts.models import UserProfile, Account

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['scenarios_attempted', 'scenarios_attempted_score',
                    'user_powerwords', 'user_weakwords', 'competency_score', 'current_level']
        

class AccountSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = Account
        fields = ['email', 'org', 'role','profile']