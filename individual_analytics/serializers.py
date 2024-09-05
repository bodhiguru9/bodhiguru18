from rest_framework import serializers
from accounts.models import UserProfile, Account

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['scenarios_attempted', 'noscenarios_attempted', 'user_powerwords', 'user_weakwords', 'competency_score']

class AccountSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = Account
        fields = ['email', 'org', 'role','profile']