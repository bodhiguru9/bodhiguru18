from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.models import UserProfile
from individual_analytics.serializers import UserProfileSerializer
from .permissions import IsAdminOrSubAdmin

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
    
    def get_queryset(self):
        user = self.request.user
        # Access sub_org via the UserProfile's related account
        sub_org = user.userprofile.account.sub_org
        return UserProfile.objects.filter(account__sub_org=sub_org)