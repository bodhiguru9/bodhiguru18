from rest_framework import serializers

from industry.models import Industry
from industry.serializers import IndustrySerializer
from orgss.models import Org, SubOrg1, Role1

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'description', 'industry', 'validity', 'is_active', 'number_of_logins']

class OrgListSerializer(serializers.ModelSerializer):
    industry = serializers.SerializerMethodField()
    
    def get_industry(self, obj):
        instance = Industry.objects.get(id=obj.industry.id)
        return IndustrySerializer(instance).data
    
    class Meta:
        model = Org
        fields = ['id', 'name', 'description', 'industry', 'validity', 'is_active', 'number_of_logins']

class SubOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubOrg1
        fields = ['id', 'name', 'description', 'org']
        
class SubOrgListSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SubOrg1
        fields = ['id', 'name', 'description', 'org']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role1
        fields = ['id', 'role_type', 'suborg']
        
class RoleListSerializer(serializers.ModelSerializer):
    suborg = serializers.SerializerMethodField()
    
    def get_suborg(self, obj):
        instance = SubOrg1.objects.get(id=obj.suborg.id)
        return SubOrgListSerializer(instance).data
    
    class Meta:
        model = Role1
        fields = ['id', 'role_type', 'suborg']
