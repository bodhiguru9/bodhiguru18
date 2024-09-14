from rest_framework import serializers
from .models import Upgrade, Upgradedetail
from orgss.models import Org

class UpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upgrade
        fields = ['id', 'name', 'description','cost']

class UpgradedetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upgradedetail
        fields = ['id', 'org', 'package', 'created_at', 'transaction_details']

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'validity', 'number_of_logins', 'package_purchased']