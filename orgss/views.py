from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from orgss.models import Org, SubOrg1, Role1, Weightage
from orgss.serializers import (OrgSerializer, OrgListSerializer, OrgAdminSerializer, SubOrgAdminSerializer,
                                SubOrgSerializer, SubOrgListSerializer, RoleSerializer, RoleListSerializer, 
                               WeightageSerializer, OrgExpirySerializer )

from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly, IsSubAdminOrReadOnly, IsAdminOrSubAdmin

from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action

from rest_framework.views import APIView

from accounts.models import Account

from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from rest_framework.decorators import api_view



class OrgViewSet(viewsets.ModelViewSet):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]


class SubOrgViewSet(viewsets.ModelViewSet):
    queryset = SubOrg1.objects.all()
    serializer_class = SubOrgSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is an admin, allow them to see sub-orgs linked to their org
        if user.is_admin:
            return SubOrg1.objects.filter(org=user.org)

        # For non-admin users, check the role
        user_role = user.role
        if user_role and user_role.role_type == 'admin':
            # Admin of a sub-org, can see all sub-orgs in their org
            return SubOrg1.objects.filter(org=user_role.suborg.org)
        elif user_role and user_role.role_type == 'sub-admin':
            # Sub-admin can only see their own sub-org
            return SubOrg1.objects.filter(id=user_role.suborg.id)

        return SubOrg1.objects.none()



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role1.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is an admin, allow them to see roles linked to their org
        if user.is_admin:
            return Role1.objects.filter(suborg__org=user.org)

        # For non-admin users, check the role
        user_role = user.role
        if user_role and user_role.role_type == 'admin':
            # Admin of a sub-org, can see all roles in their org
            return Role1.objects.filter(suborg__org=user_role.suborg.org)
        elif user_role and user_role.role_type == 'sub-admin':
            # Sub-admin can only see roles in their sub-org
            return Role1.objects.filter(suborg=user_role.suborg)

        return Role1.objects.none()


class OrgAdminViewSet(viewsets.ModelViewSet):
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_email = self.request.user.email  # Assuming the user’s email is available in the request
        try:
            user_account = Account.objects.get(email=user_email)
            org = Org.objects.get(id=user_account.org.id)

            # Check if org is expiring in 7 days
            days_since_creation = (timezone.now() - org.created_at).days
            days_left = org.validity - days_since_creation

            if days_left <= 7:
                self.send_expiry_email(user_email, org.name, days_left)

                # Add warning message to the response
                warning_message = f"Your organization's subscription will expire in {days_left} days. Please upgrade to continue using the service."

                return Response({'message': warning_message}, status=status.HTTP_200_OK)

            return Org.objects.filter(id=user_account.org.id)
        except Account.DoesNotExist:
            return Org.objects.none()

    def get_object(self):
        user_email = self.request.user.email
        try:
            user_account = Account.objects.get(email=user_email)
            return Org.objects.get(id=user_account.org.id)
        except (Account.DoesNotExist, Org.DoesNotExist):
            return None

    def send_expiry_email(self, user_email, org_name, days_left):
        # Email content
        subject = f"Your organization {org_name} is about to expire"
        message = f"""
        Dear User,

        Your organization's subscription for {org_name} is about to expire in {days_left} days.
        To continue using the service, please upgrade your plan.

        Best regards,
        Your Company Name
        """

        # Send email to the user and the admin
        recipient_list = [user_email, 'arindam@bodhiguru.com']
        send_mail(subject, message, from_email='hello@bodhiguru.com', recipient_list=recipient_list, fail_silently=False)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only permissions for everyone

        user = request.user
        if user.is_authenticated:
            try:
                # Retrieve the user's profile and check the role from the related Account model
                user_profile = user.userprofile  # Assuming the userprofile is linked via OneToOneField
                account = user_profile.user  # Access the Account model via the `user` field
                role = account.role  # Assuming `role` is a ForeignKey on the Account model
                
                # Check if the role is admin or sub-admin for the relevant suborg
                suborg_id = request.data.get('suborg')
                if role.suborg.id == int(suborg_id) and role.role_type in ['admin', 'sub-admin']:
                    return True
            except AttributeError:
                # If there is no profile, account, or role, deny permission
                return False

        return False

class WeightageViewSet(viewsets.ModelViewSet):
    queryset = Weightage.objects.all()
    serializer_class = WeightageSerializer
    permission_classes = [IsAdminOrReadOnly]


@api_view(['GET'])
def org_expiry_view(request):
    # Get all organizations with expiry information
    orgs = Org.objects.all()
    serializer = OrgExpirySerializer(orgs, many=True)
    return Response(serializer.data)