from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.serializers import (SignUpSerializer, UserSerializer, LoginSerializer, UserSerializer,
                                    profileSerializer, WelcomeEmailSerializer, RegisterSerializer,
                                    UserProfileSerializer1, UserProfileSerializer, AccountSerializer,
                                    CSVUploadSerializer, CSVDownloadSerializer, AccountORgSerializer,
                                    AccountAdminSerializer, AccountRegisterSerializer,
                                    PasswordResetRequestSerializer, PasswordResetConfirmSerializer)
from accounts.models import Account, Profile, EmailConfirmationToken, UserProfile
from django.contrib.auth.hashers import make_password
from rest_framework import status, generics, permissions, viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework.views import APIView
from accounts.utils import send_confirmation_email
from rest_framework.exceptions import PermissionDenied

from orgss.models import Org, SubOrg1
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from django.http import HttpResponse

from rest_framework.parsers import MultiPartParser
from .serializers import BulkUserUploadSerializer

import csv
from .permissions import IsAdminOrSubAdminOfOrg

from django.contrib.sites.shortcuts import get_current_site
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.utils.timezone import now

from rest_framework.decorators import action
from io import StringIO
from rest_framework.permissions import AllowAny
from django.db.models import Q

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import get_user_model


User = get_user_model()


@api_view(['POST'])
def register(request):
    request_data = {
        'first_name': request.data.get('first_name'),
        'last_name': request.data.get('last_name'),
        'password': request.data.get('password'),
        'email': request.data.get('email'),
        'username': request.data.get('username'),
        'contact_number': request.data.get('contact_number'),
    }
    try:
        default_org = Org.objects.get(name__icontains="bodhigru")
        request_data['org'] = default_org.id
    except Org.DoesNotExist:
        request_data['org'] = None
    
    serializer = SignUpSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        response = {
            'status': 'success',
            'message': 'User registered successfully'
        }
        return Response(response, status=status.HTTP_201_CREATED)
    response = {
        'status': 'failed',
        'message': serializer.errors
    }
    return Response(response, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Check if the user's organization is still valid
        if not user.org.is_active:
            raise ValidationError("Your organization is disabled. Contact your administrator.")

        # Optionally, check user validity as well
        signup_date = user.date_joined
        if timezone.now() > signup_date + timedelta(days=user.validity):
            raise ValidationError("Your account validity has expired.")

        # Add additional data to the response
        data.update({
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'org': {
                    'name': user.org.name,
                    'industry': user.org.industry,
                    'validity': user.org.validity,
                    'is_active': user.org.is_active,
                },
                'validity': user.validity,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_role': user.user_role,
                'is_email_confirmed': user.is_email_confirmed,
                'active': user.active
            },
            'status': 'success',
            'message': 'User logged in successfully.'
        })

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
def check_org_validity(request):
    current_date = timezone.now()
    orgs_to_disable = Org.objects.filter(is_active=True, validity__lte=(current_date - timezone.timedelta(days=30)))
    
    for org in orgs_to_disable:
        org.is_active = False
        org.save()

        # Disable associated users
        Account.objects.filter(org=org).update(is_active=False)

        # Send email to admin
        send_mail(
            'Organization Disabled',
            'The organization {} has been disabled.'.format(org.name),
            'arindam@bodhiguru.com',
            ['arindam@bodhiguru.com'],
            fail_silently=False,
        )

    return Response({'status': 'Checked for expired orgs and disabled them if necessary'}, status=status.HTTP_200_OK)

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def current_user(request):

    user = UserSerializer(request.user)

    return Response(user.data)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


class UserInformationAPIVIew(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        user = request.user
        email = user.email
        is_email_confirmed = user.is_email_confirmed
        payload = {'email': email, 'is_email_confirmed': is_email_confirmed, 'id': user.pk}
        return Response(data=payload, status=status.HTTP_200_OK)

class SendEmailConfirmationTokenAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):

        user = request.user
        token = EmailConfirmationToken.objects.create(user=user)
        
        send_confirmation_email(email=user.email, token_id=token.pk, user_id=user.pk)
        
        response = {
            'status': 'success',
            'message': 'Your confirmation Email was sent successfully',
        }
        
        return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    user_id = request.GET.get('user_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        data = {'is_email_confirmed': True}
        return Response({'message': 'Email has been confirmed'}, status=status.HTTP_200_OK )
       #return render(request, template_name='users/confirm_email_view.html', context=data)
    except EmailConfirmationToken.DoesNotExist:
        data = {'is_email_confirmed': False}
        return Response({'message': 'Email has not been confirmed'} )
        #return render(request, template_name='users/confirm_email_view.html', context=data)


class SendWelcomeEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WelcomeEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = Account.objects.get(email=email)
            
            # Send welcome email
            subject = 'Welcome to Our Service!'
            message = f'Hi {user.username},\n\nThank you for confirming your email. Welcome aboard!'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)
            

            return Response({'message': 'Welcome email sent successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        if email and password:
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                response = {
                    'status': 'failed',
                    'message': 'User does not exist'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            if user and user.check_password(password) and user.active == True:
                refresh = RefreshToken.for_user(user)
                user_data = LoginSerializer(user).data
                
                response = {
                    'status': 'success',
                    'message': 'User logged in successfully',
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': user_data,
                    }
                }
                
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': 'failed',
                    'message': 'Your Account has been deactivated. Please contact the admin for assistance.'
                }
                
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        elif username and password:
            try:
                user = Account.objects.get(username=username)
            except Account.DoesNotExist:
                response = {
                    'status': 'failed',
                    'message': 'User does not exist'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            
            if user and user.check_password(password) and user.active == True:
                refresh = RefreshToken.for_user(user)
                user_data = LoginSerializer(user).data
                
                response = {
                    'status': 'success',
                    'message': 'User logged in successfully',
                    'data': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': user_data,
                    }
                }
                
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': 'failed',
                    'message': 'Your Account has been deactivated. Please contact the admin for assistance.'
                }
                
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response  = {
            'status': 'failed',
            'message': 'Please provide both username/email and password'
        }
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save user and get the user instance

            # Send the welcome email to the user and the additional email to arindam@bodhiguru.com
            self.send_welcome_email(user.email, user.org.name)

            return Response({'message': 'User registered successfully', 'is_active': True, 'is_admin': user.is_admin}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_welcome_email(self, user_email, org_name):
        # Compose the email content
        subject = 'Welcome to Our Platform'
        message = f"""
        Dear User,

        Welcome to Bodhiguru!

        Your organization has been registered successfully and is valid for 30 days. 
        If you wish to continue using the service after 30 days, please consider upgrading your plan.

        Our Customer Success Team will connect with you shortly to help you get the maximum benefit from the platform.

        Best regards,
        Your Company Name
        """
        from_email = settings.DEFAULT_FROM_EMAIL

        # Email recipients
        user_recipients = [user_email]
        admin_recipient = ['arindam@bodhiguru.com']

        # Send the email to the user
        send_mail(subject, message, from_email, user_recipients, fail_silently=False)

        # Send the email to Arindam
        admin_message = f"A new user has registered under the organization: {org_name}."
        send_mail(subject="New User Registration", message=admin_message, from_email=from_email, recipient_list=admin_recipient, fail_silently=False)



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Check if the user's organization is valid
        if not user.org.is_active:
            raise ValidationError("Your organization is disabled. Contact your administrator.")
        
        org_expiration_date = user.org.created_at + timedelta(days=user.org.validity)
        if timezone.now() > org_expiration_date:
            user.org.is_active = False
            user.org.save()
            raise ValidationError("Your organization's validity has expired.")

        # Check if the user's validity is still active
        user_expiration_date = user.date_joined + timedelta(days=user.validity)
        if timezone.now() > user_expiration_date:
            raise ValidationError("Your account validity has expired. Contact your administrator.")

        # Add additional data to the response
        data.update({
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                #'user_role': user.role,
                'org': {
                    'name': user.org.name,
                    'id': user.org.id,
                    'validity': user.org.validity,
                    'is_active': user.org.is_active,
                },
                'validity': user.validity,
            },
            'status': 'success',
            'message': 'User logged in successfully.'
        })

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  

class IsAdminOfOrgOrSubOrg(permissions.BasePermission):
    """
    Custom permission to check if the user is an admin of the org or sub-org.
    """
    def has_permission(self, request, view):
        # Assuming you have a way to determine if a user is an admin
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        # Only allow if the admin belongs to the same org/sub-org as the user being viewed
        return obj.org == request.user.org or obj.sub_org == request.user.sub_org




class UserListView(generics.ListAPIView):
    """
    Admin can view the list of users within their org/sub-org.
    """
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOfOrgOrSubOrg]

    def get_queryset(self):
        user = self.request.user
        # Filter by both org and sub_org
        return Account.objects.filter(Q(org=user.org) & Q(sub_org=user.sub_org))






class UserUpdateView(generics.RetrieveUpdateAPIView):
    """
    Admin can update user details in their org/sub-org.
    """
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOfOrgOrSubOrg]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(org=user.org, sub_org=user.sub_org)

class DisableUserView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrSubAdminOfOrg]  # Apply custom permission

    def update(self, request, *args, **kwargs):
        account = self.get_object()
        if account.validity <= 0:  # Validity expires when it hits 0 or negative
            # Disable user and user profile
            account.is_active = False
            account.save()
            user_profile = UserProfile.objects.get(user=account)
            user_profile.is_active = False
            user_profile.save()
            return Response({"message": "User disabled after validity expired"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User validity is still valid"}, status=status.HTTP_400_BAD_REQUEST)


class EnableUserView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Get the user instance to be updated
        user = self.get_object()

        # Check if user is linked to an organization
        if not user.org:
            return Response({"error": "User is not associated with an organization."}, status=status.HTTP_400_BAD_REQUEST)

        org = user.org

        # Check if the org is still valid
        if not org.is_active:
            return Response({"error": "Organization is not active."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if org.expires_on is not None and if the expiry date is in the past
        if org.expires_on and org.expires_on < timezone.now().date():
            return Response({"error": "Organization validity has expired."}, status=status.HTTP_400_BAD_REQUEST)

        # Check the number of active logins in the organization
        active_user_count = Account.objects.filter(org=org, is_active=True).count()
        if active_user_count >= org.number_of_logins:
            return Response({"error": "Maximum number of active logins for this organization has been reached."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the extended_days from request data
        extended_days = request.data.get('extended_days', None)

        # Validate the extended_days field
        if extended_days is None:
            return Response({"error": "Extended days field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            extended_days = int(extended_days)
        except ValueError:
            return Response({"error": "Extended days must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if extended_days is a multiple of 30
        if extended_days % 30 != 0:
            return Response({"error": "Extended days must be a multiple of 30."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate new user expiry date and compare with the org expiry date
        new_user_expiry = timezone.now().date() + timedelta(days=extended_days)
        if org.expires_on and new_user_expiry > org.expires_on:
            return Response({"error": "User's validity extension cannot exceed the organization's validity."}, status=status.HTTP_400_BAD_REQUEST)

        # If valid, proceed with updating the user's validity
        user.validity += extended_days
        user.is_active = True  # Set user as active
        user.save()

        # Update the related UserProfile model
        user_profile = user.userprofile
        user_profile.is_active = True
        user_profile.save()

        return Response({"success": "User enabled successfully."}, status=status.HTTP_200_OK)


"""
class EnableUserView(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrSubAdminOfOrg]  # Apply custom permission

    def update(self, request, *args, **kwargs):
        # Get the user instance to be updated
        user = self.get_object()

        # Extract the extended_days from request data
        extended_days = request.data.get('extended_days', None)

        # Validate the extended_days field
        if extended_days is None:
            return Response({"error": "Extended days field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            extended_days = int(extended_days)
        except ValueError:
            return Response({"error": "Extended days must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if extended_days is a multiple of 30
        if extended_days % 30 != 0:
            return Response({"error": "Extended days must be a multiple of 30."}, status=status.HTTP_400_BAD_REQUEST)

        # If valid, proceed with updating the user's validity
        user.validity += extended_days
        user.is_active = True  # Set user as active
        user.save()

        # Update the related UserProfile model
        user_profile = user.userprofile
        user_profile.is_active = True
        user_profile.save()

        return Response({"success": "User enabled successfully."}, status=status.HTTP_200_OK)
"""
#csv for bulk upload

class AccountViewSet(viewsets.ViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin or user.role.role_type in ['admin', 'sub-admin']:
            return Account.objects.filter(org=user.org, sub_org=user.sub_org)
        return Account.objects.none()

    @action(detail=False, methods=['get'], url_path='download-csv')
    def download_csv(self, request):
        user = request.user

        # Check if user has permission based on 'is_admin' or 'role'
        if not user.is_admin and not (user.role and user.role.role_type in ['admin', 'sub-admin']):
            return Response({"error": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)

        org_name = user.org.name
        sub_org_name = user.sub_org.name if user.sub_org else "N/A"
        
        # Define the CSV headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{org_name}_{sub_org_name}_users.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['first_name', 'last_name', 'email', 'username'])  # Headers
        
        # Fetch users under this org and sub-org
        users = Account.objects.filter(org=user.org, sub_org=user.sub_org)
        for account in users:
            writer.writerow([account.first_name, account.last_name, account.email, account.username])
        
        return response

    @action(detail=False, methods=['post'], url_path='upload-csv')
    def upload_csv(self, request):
        user = request.user

        # Check if user has permission based on 'is_admin' or 'role'
        if not user.is_admin and not (user.role and user.role.role_type in ['admin', 'sub-admin']):
            return Response({"error": "You are not authorized"}, status=status.HTTP_403_FORBIDDEN)

        org = user.org
        sub_org = user.sub_org

        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['file']
            csv_data = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_data)

            accounts_created = []
            errors = []

            for row in csv_reader:
                try:
                    account = Account(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        email=row['email'],
                        username=row['username'],
                        org=org,  # Assign org of admin/sub-admin
                        sub_org=sub_org,  # Assign sub-org of admin/sub-admin
                        contact_number='9999999999',  # Default contact number
                    )
                    account.set_password('123Zola$$Ts')  # Set the default password
                    account.save()
                    accounts_created.append(account.email)
                except Exception as e:
                    errors.append({"email": row['email'], "error": str(e)})

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"created": accounts_created}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountAdminViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role.role_type in [Role.ADMIN, Role.SUB_ADMIN]:
            return Account.objects.filter(org=user.org)
        return Account.objects.none()
    

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            reset_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uidb64}/{token}/"

            # Send email
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data={
            'uidb64': uidb64,
            'token': token,
            'new_password': request.data.get('new_password')
        })

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    