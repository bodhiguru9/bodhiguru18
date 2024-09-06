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
        # Get the UserProfile instance based on the pk provided
        try:
            user_profile = UserProfile.objects.get(pk=self.kwargs['pk'])
        except UserProfile.DoesNotExist:
            raise NotFound("UserProfile not found.")
        
        # Retrieve the related Account based on email or user_id from the profile's user
        account = Account.objects.filter(email=user_profile.user.email).first()  # Adjust this if user_id is used
        
        # Check the account role permissions
        request_user_account = Account.objects.filter(email=self.request.user.email).first()
        if request_user_account and request_user_account.role.role_type in ['admin', 'sub-admin']:
            return user_profile  # Return the profile if the user has permission
        
        raise PermissionDenied("You don't have permission to view this user's details.")