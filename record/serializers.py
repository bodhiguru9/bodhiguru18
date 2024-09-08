from rest_framework import serializers

class OrgReportSerializer(serializers.Serializer):
    org_name = serializers.CharField()
    user_count = serializers.IntegerField()
    #items_responded = serializers.IntegerField()
    total_scenarios_attempted = serializers.IntegerField()
   