from rest_framework import serializers
from orgss.models import SubOrg
from accounts.models import UserProfile

class UserCompetencySerializer(serializers.Serializer):
    competency_name = serializers.CharField()
    percentile = serializers.FloatField()

class SubOrgAnalyticsSerializer(serializers.ModelSerializer):
    total_users = serializers.SerializerMethodField()
    total_scenarios_attempted = serializers.SerializerMethodField()
    total_scenarios_per_user = serializers.SerializerMethodField()
    user_competency_leaderboard = serializers.SerializerMethodField()

    class Meta:
        model = SubOrg
        fields = ['id', 'name', 'total_users', 'total_scenarios_attempted', 'total_scenarios_per_user', 'user_competency_leaderboard']

    def get_total_users(self, obj):
        return obj.suborgrole.count()

    def get_total_scenarios_attempted(self, obj):
        total_scenarios = 0
        for role in obj.suborgrole.all():
            total_scenarios += role.user.userprofile.scenarios_attempted
        return total_scenarios

    def get_total_scenarios_per_user(self, obj):
        scenarios_per_user = {}
        for role in obj.suborgrole.all():
            user = role.user
            scenarios_per_user[user.username] = user.userprofile.scenarios_attempted
        return scenarios_per_user

    def get_user_competency_leaderboard(self, obj):
        # Implement logic to calculate percentile based on competency scores
        # Example logic, replace with actual implementation
        leaderboard = []
        users = obj.suborgrole.all()
        total_users = len(users)
        
        # Assuming competency_scores is a JSONField storing competency scores
        all_competencies = set()
        for user in users:
            all_competencies.update(user.userprofile.competency_scores.keys())

        for competency in all_competencies:
            competency_scores = []
            for user in users:
                if competency in user.userprofile.competency_scores:
                    competency_scores.append(user.userprofile.competency_scores[competency])
            
            competency_scores.sort(reverse=True)  # Sort scores in descending order
            user_percentiles = {}
            for score in competency_scores:
                percentile = (competency_scores.index(score) + 1) / total_users * 100
                user_percentiles[score] = percentile

            leaderboard.append({
                'competency_name': competency,
                'percentiles': user_percentiles
            })
        
        return leaderboard