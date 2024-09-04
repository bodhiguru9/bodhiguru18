from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.serializers import SignUpSerializer, UserSerializer, profileSerializer, WelcomeEmailSerializer
from accounts.models import Account, Profile, EmailConfirmationToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from django.core.mail import send_mail, EmailMessage
from datetime import datetime, timedelta

from rest_framework.views import APIView
from accounts.utils import send_confirmation_email
from accounts.serializers import LoginSerializer
from orgss.models import Org
from django.conf import settings

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
