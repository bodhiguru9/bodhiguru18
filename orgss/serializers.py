from rest_framework import serializers

from industry.models import Industry
from industry.serializers import IndustrySerializer
from orgss.models import Org, SubOrg, Role

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'description', 'industry']

class OrgListSerializer(serializers.ModelSerializer):
    industry = serializers.SerializerMethodField()
    
    def get_industry(self, obj):
        instance = Industry.objects.get(id=obj.industry.id)
        return IndustrySerializer(instance).data
    
    class Meta:
        model = Org
        fields = ['id', 'name', 'description', 'industry']

class SubOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubOrg
        fields = ['id', 'name', 'description', 'org']
        
class SubOrgListSerializer(serializers.ModelSerializer):
    org = serializers.SerializerMethodField()
    
    def get_org(self, obj):
        instance = Org.objects.get(id=obj.org.id)
        return OrgListSerializer(instance).data
    
    class Meta:
        model = SubOrg
        fields = ['id', 'name', 'description', 'org']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'suborg']
        
class RoleListSerializer(serializers.ModelSerializer):
    suborg = serializers.SerializerMethodField()
    
    def get_suborg(self, obj):
        instance = SubOrg.objects.get(id=obj.suborg.id)
        return SubOrgListSerializer(instance).data
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'suborg']
