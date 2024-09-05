from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, UserProfileSerializer
from accounts.models import Account, UserProfile
from .permissions import IsAdminOrSubAdmin
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]
    serializer_class = AccountSerializer

    def get_queryset(self):
        # Get the admin/sub_admin's org using their email
        account = get_object_or_404(Account, email=self.request.user.email)
        sub_org = self.request.query_params.get('sub_org')
        
        if sub_org:
            # Return users within the same org and filtered by sub_org
            return Account.objects.filter(org=account.org, sub_org_id=sub_org)
        
        # Return users within the same org
        return Account.objects.filter(org=account.org)

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # Retrieve the user profile by email and ensure they are part of the same org/sub-org
        email = self.kwargs['email']
        user_profile = get_object_or_404(UserProfile, user__email=email)
        
        # Get the admin/sub_admin's org using their email
        account = get_object_or_404(Account, email=self.request.user.email)

        # Check if the user belongs to the same org
        if user_profile.user.account.org == account.org:
            return user_profile
        else:
            raise PermissionDenied("You do not have permission to view this user's data.")