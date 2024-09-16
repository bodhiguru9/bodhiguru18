from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from orgss.models import Org, SubOrg1, Role1
from orgss.serializers import (OrgSerializer, OrgListSerializer, OrgAdminSerializer, SubOrgAdminSerializer,
                                SubOrgSerializer, SubOrgListSerializer, RoleSerializer, RoleListSerializer
                               )

from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly, IsSubAdminOrReadOnly

from rest_framework import viewsets
from rest_framework.decorators import action

from rest_framework import generics, permissions

from rest_framework.views import APIView

from accounts.models import Account

from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta


class OrgViewSet(viewsets.ModelViewSet):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]

class SubOrgViewSet(viewsets.ModelViewSet):
    queryset = SubOrg1.objects.all()
    serializer_class = SubOrgSerializer
    permission_classes = [IsAuthenticated]

    # Admin or sub-admin can only access sub-orgs linked to their org/sub-org
    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            return SubOrg1.objects.filter(org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            return SubOrg1.objects.filter(id=user_role.suborg.id)
        return SubOrg1.objects.none()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role1.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    # Admin or sub-admin can only access roles linked to their org/sub-org
    def get_queryset(self):
        user_role = self.request.user.role
        if user_role.role_type == 'admin':
            return Role1.objects.filter(suborg__org=user_role.suborg.org)
        elif user_role.role_type == 'sub-admin':
            return Role1.objects.filter(suborg=user_role.suborg)
        return Role1.objects.none()

"""
class OrgAdminViewSet(viewsets.ModelViewSet):
    serializer_class = OrgSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_email = self.request.user.email  # Assuming the user’s email is available in the request
        try:
            user_account = Account.objects.get(email=user_email)
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
"""

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