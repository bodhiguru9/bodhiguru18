
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied
from django.db import models

from accounts.models import UserProfile, Account
from orgss.models import Org, SubOrg1, Role1
from .serializers import UserProfileSerializer, UserAnalyticsSerializer, UserScenarioDetailSerializer


class OrgAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, org_id=None, suborg_id=None):
        # Get the current user's profile and role
        current_user_profile = UserProfile.objects.get(user=request.user)
        current_account = current_user_profile.user
        user_role = current_account.role.role_type if current_account.role else None

        # Check access based on `is_admin` or the role
        if current_account.is_admin:
            # Allow if the user is a super admin, even if their role is blank
            pass
        elif user_role not in ['admin', 'sub-admin']:
            # Allow only if the role is admin or sub-admin
            raise PermissionDenied(detail="You do not have permission to view this data.")

        # Get the org and suborg
        org = Org.objects.get(id=org_id)
        suborg = SubOrg1.objects.get(id=suborg_id) if suborg_id else None

        # Filter users based on the org and sub-org
        if suborg:
            users = UserProfile.objects.filter(user__role__suborg=suborg)
        else:
            users = UserProfile.objects.filter(user__role__suborg__org=org)

        # Total number of users
        total_users = users.count()

        # Sum total of scenarios attempted by all users
        total_scenarios_attempted = users.aggregate(total_attempts=models.Sum('scenarios_attempted'))['total_attempts'] or 0

        # Individual user details (scenarios attempted per user)
        user_data = UserScenarioDetailSerializer(users, many=True).data

        response_data = {
            'total_users': total_users,
            'total_scenarios_attempted': total_scenarios_attempted,
            'users': user_data
        }

        return Response(response_data)