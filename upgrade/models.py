from django.db import models
from orgss.models import Org

class Upgrade(models.Model):
    PACKAGE_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
    
    name = models.CharField(max_length=50, choices=PACKAGE_CHOICES)
    description = models.TextField(null=True, blank=True)
    cost = models.IntegerField(default=0)  # Package cost

    def __str__(self):
        return self.name

class Upgradedetail(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE)
    upgrade = models.ForeignKey(Upgrade, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_details = models.TextField()

    def __str__(self):
        return f"{self.org} - {self.upgrade}"