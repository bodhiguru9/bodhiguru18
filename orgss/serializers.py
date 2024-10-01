from rest_framework import serializers

from industry.models import Industry
from industry.serializers import IndustrySerializer
from orgss.models import Org, SubOrg1, Role1, Weightage

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'description', 'logo', 'industry', 'validity', 'is_active', 'number_of_logins', 'package_purchased']

class OrgListSerializer(serializers.ModelSerializer):
    industry = serializers.SerializerMethodField()
    
    def get_industry(self, obj):
        instance = Industry.objects.get(id=obj.industry.id)
        return IndustrySerializer(instance).data
    
    class Meta:
        model = Org
        fields = ['id', 'name', 'description', 'logo', 'industry', 'validity', 'is_active', 'number_of_logins', 'package_purchased']

class SubOrgSerializer(serializers.ModelSerializer):
    org = serializers.SlugRelatedField(queryset=Org.objects.all(), slug_field='name')
    org_id = serializers.IntegerField(source='org.id', read_only=True)


    class Meta:
        model = SubOrg1
        fields = ['id', 'name', 'description', 'org_id', 'org']
        
class SubOrgListSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SubOrg1
        fields = ['id', 'name', 'description', 'org']

class RoleSerializer(serializers.ModelSerializer):
    suborg = serializers.SlugRelatedField(queryset=SubOrg1.objects.all(), slug_field='name')

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

class OrgAdminSerializer(serializers.ModelSerializer):
    suborgs = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Org
        fields = ['id', 'name', 'suborgs']

class SubOrgAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubOrg1
        fields = ['id', 'name', 'org']

class WeightageSerializer(serializers.ModelSerializer):
    suborg_name = serializers.SerializerMethodField()
    competency_name = serializers.SerializerMethodField()

    class Meta:
        model = Weightage
        fields = ['id','suborg', 'suborg_name', 'competency', 'competency_name', 'weightage']
        read_only_fields = ['suborg', 'suborg_name', 'competency', 'competency_name']  # suborg and competency should be read-only in PUT/PATCH requests

    def get_suborg_name(self, obj):
        return obj.suborg.name if obj.suborg else None

    def get_competency_name(self, obj):
        return obj.competency.competency_name if obj.competency else None

class OrgExpirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['name', 'expires_on', 'is_active'] 

