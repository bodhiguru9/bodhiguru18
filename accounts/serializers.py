from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import Account, Profile, EmailConfirmationToken, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from orgss.models import Org

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        fields = ['email', 'first_name', 'last_name', 'password', 'username']
        
    def create(self, validated_data):
        user = Account.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                #contact_number=validated_data['contact_number'],
                #org=validated_data.get('org'),
                )
        user.set_password(validated_data['password'])
        user.save()
        return user

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'industry', 'validity', 'is_active']

class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()
    org = OrgSerializer()
    
    class Meta:
        model = Account
        fields = ['id', 'email', 'first_name', 'contact_number', 'last_name', 'validity', 'username', 'role', 'org', 'is_email_confirmed', 'is_active', 'active', 'user_role']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"

class WelcomeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = Account.objects.get(email=value)
            token_exists = EmailConfirmationToken.objects.filter(user=user).exists()
            if not token_exists:
                raise serializers.ValidationError("No confirmation token exists for this user.")
            return value
        except Account.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.") 



class BulkUserUploadSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    #contact_number = serializers.CharField(max_length=15)

    def create(self, validated_data):
        # Ensure the email is unique
        if Account.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(f"Email {validated_data['email']} is already in use.")
        
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            password=validated_data['password'],
            #contact_number=validated_data['contact_number']
        )
        return user

class RegisterSerializer(serializers.ModelSerializer):
    org_name = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name', 'contact_number', 'org_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        org_name = validated_data.pop('org_name')
        org, created = Org.objects.get_or_create(name=org_name)
        
        user = Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_number=validated_data['contact_number'],
            org=org,
            password=validated_data['password']
        )
        return user      

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields ="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'is_active']