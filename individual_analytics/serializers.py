from rest_framework import serializers
from accounts.models import UserProfile, Account
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['scenarios_attempted', 'scenarios_attempted_score', 'user_powerwords', 'user_weakwords', 'competency_score', 'current_level']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

class UserSerializer1(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = Account
        fields = '__all__'      