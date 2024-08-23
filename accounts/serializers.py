from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import Account, Profile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class LoginSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    org = serializers.SerializerMethodField()
    
    def get_role(self, obj):
        return getattr(obj.role, 'name', None)
    
    def get_org(self, obj):
        org_name = getattr(obj.org, 'name', None)
        org_logo = None
        if hasattr(obj.org, 'logo') and obj.org.logo:
            org_logo = obj.org.logo.url
        return {'name': org_name, 'logo': org_logo}
    
    class Meta:
        model = Account
        exclude = (
            'password', 'last_login', 'is_active', 'is_staff', 'date_joined',
            'is_admin', 'is_superadmin', 
        )

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Account.objects.all())]
            )
    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=Account.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password', 'org', 'username']
        
    def create(self, validated_data):
        user = Account.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                org=validated_data.get('org'),
                )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()
    
    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'role', 'is_email_confirmed', 'user_role']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"