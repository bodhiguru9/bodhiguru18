from rest_framework import serializers
from .models import Upgrade, Upgradedetail
from orgss.models import Org

class UpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upgrade
        fields = '__all__'

class UpgradedetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upgradedetail
        fields = '__all__'

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'validity', 'number_of_logins', 'package_purchased']

class PurchaseSerializer(serializers.Serializer):
    org_id = serializers.IntegerField()  # Accept org_id from the client side
    number_of_packs = serializers.IntegerField(required=False, default=1)         