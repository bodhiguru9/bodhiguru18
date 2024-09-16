from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.models import UserProfile, Account
from individual_analytics.serializers import UserProfileSerializer
from .permissions import IsAdminOrSubAdmin
from rest_framework.exceptions import NotFound

class UserListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]
    
    def get_queryset(self):
        user = self.request.user  # Assuming user is linked to the Account model
        # Access sub_org via the UserProfile's related account
        sub_org = user.userprofile.user.sub_org
        return UserProfile.objects.filter(user__sub_org=sub_org)
  

class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]
    
    def get_object(self):
        # Get the email from the URL
        email = self.kwargs['email']

        # Fetch the account based on the email
        account = Account.objects.filter(email=email).first()

        # Check if the current authenticated user is an admin or sub-admin
        current_user_profile = self.request.user.userprofile

        if account and current_user_profile.user.role.role_type in ['admin', 'sub-admin']:
            # Check if the admin or sub-admin belongs to the same sub-organization as the user
            if account.sub_org == current_user_profile.user.sub_org:
                try:
                    return UserProfile.objects.get(user=account)
                except UserProfile.DoesNotExist:
                    raise NotFound("UserProfile does not exist for this account.")
            else:
                raise PermissionDenied("You don't have permission to view users outside your sub-organization.")
        else:
            raise PermissionDenied("You don't have permission to view this user's details.")         