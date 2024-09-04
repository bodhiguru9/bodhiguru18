from rest_framework import serializers

class OrganizationReportSerializer(serializers.Serializer):
    organization_name = serializers.CharField()
    user_count = serializers.IntegerField()
    items_responded = serializers.IntegerField()