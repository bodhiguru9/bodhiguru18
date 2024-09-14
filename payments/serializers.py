from rest_framework import serializers
from .models import Package, PackageDetail

from orgss.models import Org

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'description', 'cost']

class PackageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageDetail
        fields = ['id', 'org', 'package', 'created_at', 'transaction_details']

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = ['id', 'name', 'validity', 'number_of_logins', 'package_purchased']        