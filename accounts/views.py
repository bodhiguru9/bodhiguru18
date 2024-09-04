from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.serializers import SignUpSerializer, UserSerializer, profileSerializer, WelcomeEmailSerializer
from accounts.models import Account, Profile, EmailConfirmationToken
from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework.views import APIView
from accounts.utils import send_confirmation_email
from accounts.serializers import LoginSerializer
from orgss.models import Org
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

import csv

from django.contrib.sites.shortcuts import get_current_site

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

@api_view(['POST']) 
def forgot_password(request):

    data = request.data
    user = get_object_or_404(Account, email = data['email'])

    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes = 30)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date

    user.profile.save()
    serializer=profileSerializer(user.profile)

    host = get_current_host(request)

    link = "{host}accounts/reset_password/{token}".format(host=host, token=token)
    body =  "Click on the following link to reset your password {link}".format(link=link)

    send_mail(
        "Password reset link for Bodhiguru",
        body,
        "hello@bodhiguru.com",
        [data['email']]
    )
    return Response({'message': 'Password reset email sent to {email}'. format(email=data['email']), "profile":serializer.data })

@api_view(['POST']) 
def reset_password(request,token):
    data = request.data
    user = get_object_or_404(Account, profile__reset_password_token = token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response ({"error":"The link has expired"}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirmPassword']:
        return Response ({"error":"The passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

    user.password =  make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None

    user.profile.save()
    user.save()

    return Response({'message': 'Password has been reset'}, status=status.HTTP_200_OK)

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

"""
class BulkUserUploadAPIView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        
        # Check if the uploaded file is CSV
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'File is not CSV'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process the CSV file
        users_created = 0
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(decoded_file)
            for row in csv_reader:
                # Validate and create users
                serializer = SignUpSerializer(data=row)
                if serializer.is_valid():
                    serializer.save()

                    # Send registration email
                    user_data = serializer.data
                    send_registration_email(user_data['email'], user_data['username'], user_data['password'])

                    users_created += 1
                else:
                    # Handle serializer errors
                    pass  # Handle serializer errors here
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': f'{users_created} users created successfully.'}, status=status.HTTP_201_CREATED)

def send_registration_email(email, username, password):
    # Construct and send registration email
    subject = 'Welcome to YourApp!'
    message = f'Hi {username},\n\nWelcome to YourApp! You can access the web app using:\nURL: https://yourapp.com\nUsername: {username}\nPassword: {password}\n\nEnjoy using YourApp!'
    from_email = 'yourapp@example.com'
    send_mail(subject, message, from_email, [email])

"""    
