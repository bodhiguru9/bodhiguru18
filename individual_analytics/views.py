from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.models import UserProfile, Account
from individual_analytics.serializers import UserProfileSerializer
from .permissions import IsAdminOrSubAdmin
from rest_framework.exceptions import NotFound

class UserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # Get the currently logged-in user
        account = Account.objects.get(email=user.email)

        # Check if the user is a super admin
        if account.is_admin:
            # Fetch all users in the same org/sub-org (regardless of their role)
            return UserProfile.objects.filter(user__org=account.org)

        # If the user is not a super admin, check their role
        elif account.role.role_type in ['admin', 'sub-admin']:
            # Return users mapped to the same sub_org
            return UserProfile.objects.filter(user__sub_org=account.sub_org)

        raise PermissionDenied("You don't have permission to view this list of users.")
  

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the email from the URL
        email = self.kwargs['email']
        account = Account.objects.filter(email=email).first()

        # Fetch the current logged-in user's profile and account
        current_user = self.request.user
        current_account = Account.objects.get(email=current_user.email)

        # Check if the current user is a super admin
        if current_account.is_admin:
            # If super admin, allow access to user details within the same org
            if account and account.org == current_account.org:
                try:
                    return UserProfile.objects.get(user=account)
                except UserProfile.DoesNotExist:
                    raise NotFound("UserProfile does not exist for this account.")
            else:
                raise PermissionDenied("You don't have permission to view this user's details.")

        # If the current user is not a super admin but is admin/sub-admin, check their sub-org
        elif current_account.role.role_type in ['admin', 'sub-admin']:
            if account and account.sub_org == current_account.sub_org:
                try:
                    return UserProfile.objects.get(user=account)
                except UserProfile.DoesNotExist:
                    raise NotFound("UserProfile does not exist for this account.")
            else:
                raise PermissionDenied("You don't have permission to view users outside your sub-organization.")
        
        raise PermissionDenied("You don't have permission to view this user's details.")