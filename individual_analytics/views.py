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
from rest_framework import status


"""
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

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get(self, request, *args, **kwargs):
        try:
            # Assuming you are querying the correct UserProfile objects
            queryset = UserProfile.objects.all()  # Or any specific filtering
            if queryset.exists():
                print(queryset)
                serializer = UserProfileSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "No profiles found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
"""

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get(self, request, *args, **kwargs):
        try:
            # Get the admin user's org or sub_org
            account = Account.objects.get(email=request.user.email)
            print(f"User role: {account.role}")
            if account.role not in ['admin', 'sub_admin']:
                return Response({"error": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)

            # Filter UserProfiles by the admin's org or sub_org
            if account.sub_org:
                user_profiles = UserProfile.objects.filter(user__account__sub_org=account.sub_org)
            else:
                user_profiles = UserProfile.objects.filter(user__account__org=account.org)

            # Join UserProfile data with first_name, last_name, and email from Account model
            user_profiles_with_account_data = user_profiles.select_related('user').values(
                'user__first_name', 
                'user__last_name', 
                'user__email',
                'scenarios_attempted', 
                'scenarios_attempted_score', 
                'user_powerwords', 
                'user_weakwords', 
                'competency_score', 
                'current_level'
            )

            return Response(user_profiles_with_account_data, status=status.HTTP_200_OK)

        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSubAdmin]

    def get(self, request, email, *args, **kwargs):
        try:
            # Check if the requesting user has the necessary permissions
            if not (request.user.is_superuser or request.user.role in ['admin', 'sub_admin']):
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

