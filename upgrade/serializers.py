from rest_framework import serializers
from .models import Upgrade, Upgradedetail, UpgradeAssessment
from orgss.models import Org



class UpgradeAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpgradeAssessment
        fields = ['id', 'name', 'description', 'cost']

class UpgradeSerializer1(serializers.ModelSerializer):
    # Include the assessment packages as part of the upgrade listing
    assessment_packages = UpgradeAssessmentSerializer(many=True, read_only=True, source='assessment_package')

    class Meta:
        model = Upgrade
        fields = ['id', 'name', 'description', 'cost', 'assessment_packages']

class UpgradeSerializer(serializers.ModelSerializer):
    assessment_package = UpgradeAssessmentSerializer()

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