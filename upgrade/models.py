from django.db import models
from orgss.models import Org
from django.utils import timezone
from datetime import timedelta


class UpgradeAssessment(models.Model):
    Assessment_Package_Choices = [
        ('no_assessment', 'No MCQ Assessment'),
        ('assessment30', '30 MCQ Questions'),
        ('assessment60', '60 MCQ Questions')

    ]

    name = models.CharField(max_length=90, choices=Assessment_Package_Choices)
    description = models.TextField(null=True, blank=True)
    cost = models.IntegerField(default=0)  # Package cost

    def __str__(self):
        return self.name



class Upgrade(models.Model):
    PACKAGE_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        
    ]
    
    name = models.CharField(max_length=50, choices=PACKAGE_CHOICES)
    description = models.TextField(null=True, blank=True)
    assessment_package = models.ForeignKey(UpgradeAssessment, on_delete=models.CASCADE, related_name='upgradeassessment', default = 1)
    cost = models.IntegerField(default=0)  # Package cost

    def __str__(self):
        return self.name
"""
class Upgradedetail(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_details = models.TextField()
    #additional_logins = models.IntegerField(default=0)  # For storing additional logins for Package 9
    expires_on = models.DateField(default=timezone.now().date() + timedelta(days=30))

    def __str__(self):
        return f"{self.org} - {self.upgrade}"

"""

class Upgradedetail(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_details = models.TextField()
    expires_on = models.DateField(null=True, blank=True)  # Will be set based on package

    def save(self, *args, **kwargs):
        # Set expiry date to 365 days for both Bronze and Silver
        if self.upgrade.name in ['bronze', 'silver']:
            self.expires_on = timezone.now().date() + timedelta(days=365)

        # Ensure the org's expiry date matches the upgraded package expiry
        org = self.org
        org.expires_on = self.expires_on
        org.save()

        super(Upgradedetail, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.org} - {self.upgrade}"