from rest_framework import serializers
from accounts.models import UserProfile, Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'id','first_name', 'last_name', 'org', 'sub_org', 'role']  # Adjust according to actual fields

class UserProfileSerializer(serializers.ModelSerializer):
    account_data = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['account_data', 'scenarios_attempted', 
                  'user_powerwords', 'user_weakwords', 'competency_score', 'assessment_score', 'current_level']

    def get_account_data(self, obj):
        # Get the related Account instance via email or user_id
        account = Account.objects.filter(email=obj.user.email).first()  # Adjust to match how you relate profiles to accounts
        return AccountSerializer(account).data if account else None