from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from rest_framework.response import Response
from accounts.models import UserProfile, Account
from orgss.models import Org
from rest_framework.exceptions import PermissionDenied

class OrgAnalyticsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Get the account linked to the user
        account = Account.objects.filter(email=user.email).first()

        # Check if the user is an admin or sub-admin
        if account and account.role.role_type in ['admin', 'sub-admin']:
            org = account.org  # Assuming the user is mapped to the Org via Account
            sub_org = account.sub_org  # Assuming sub-org is accessed via Account

            # Fetch accounts that are part of the sub-org
            sub_org_accounts = Account.objects.filter(sub_org=sub_org)

            # Extract emails from the accounts in the sub-org
            sub_org_emails = sub_org_accounts.values_list('email', flat=True)

            # Fetch total number of users in the sub-org
            total_users = UserProfile.objects.filter(user__in=sub_org_emails).count()

            # Fetch total scenarios attempted in the sub-org
            total_scenarios_attempted = UserProfile.objects.filter(user__in=sub_org_emails).aggregate(total_attempts=Count('scenarios_attempted'))['total_attempts']

            # Fetch scenarios attempted per user
            scenarios_per_user = UserProfile.objects.filter(user__in=sub_org_emails).values('user').annotate(total_attempts=Count('scenarios_attempted'))
            scenarios_per_user_dict = {str(user['user']): user['total_attempts'] for user in scenarios_per_user}

            # Calculate leaderboard based on percentile score
            users_profiles = UserProfile.objects.filter(user__in=sub_org_emails).exclude(competency_score__isnull=True)
            leaderboard = []
            
            # Process leaderboard based on competency scores
            for profile in users_profiles:
                # Split and calculate percentile based on the competency scores
                competency_scores = profile.competency_score.split(',')  # Split on comma to retrieve scores
                scores = [int(score.split(':')[-1]) for score in competency_scores]  # Assuming format 'competency:score'
                average_score = sum(scores) / len(scores) if scores else 0
                
                leaderboard.append({
                    'email': profile.user,  # Return email or any identifier
                    'average_score': average_score
                })
            
            # Sort leaderboard by average score in descending order
            leaderboard = sorted(leaderboard, key=lambda x: x['average_score'], reverse=True)

            # Prepare response data
            data = {
                'total_users': total_users,
                'total_scenarios_attempted': total_scenarios_attempted,
                'scenarios_per_user': scenarios_per_user_dict,
                'leaderboard': leaderboard
            }

            return Response(data)

        raise PermissionDenied("You don't have permission to access this data.")