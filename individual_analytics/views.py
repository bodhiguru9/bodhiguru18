from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, UserProfileSerializer
from accounts.models import Account, UserProfile
from .permissions import IsAdminOrSubAdmin
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserProfileSerializer
from individual_analytics.permissions import IsAdminOrSubAdmin

from django.contrib.auth.models import User




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

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get(self, request, email, *args, **kwargs):
        try:
            # Check if the requesting user has the necessary permissions
            if not (request.user.role in ['admin', 'sub_admin']):
                raise PermissionDenied("You do not have permission to access this resource.")
            
            # Retrieve the UserProfile based on the email
            try:
                user = User.objects.get(email=email)  # Assuming `User` has the email field
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                return Response({"error": "UserProfile not found"}, status=404)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            # Serialize the UserProfile data
            serializer = UserProfileSerializer(user_profile)
            
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)