from django.db import models
from orgss.models import Org
from django.utils import timezone
from datetime import timedelta, datetime

class Package(models.Model):
    def __str__(self):
        return self.name

    PACKAGE_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('package9', 'Package 9'),
    ]
    
    name = models.CharField(max_length=50, choices=PACKAGE_CHOICES, null=True, blank=True)    
    description = models.CharField(max_length = 500, blank=True, null=True)
    cost = models.IntegerField(default=0)

class PackageDetails(models.Model):
    def __str__(self):
        return f"{self.package.name} - {self.org.name}"

    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='org_payment', null=False, blank=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package', null=False, blank=False)
    created_at = models.DateTimeField(default=datetime.now)
    transaction_details = models.CharField(max_length=500, blank=True, null=True)
    