from django.db import models

from industry.models import Industry
from competency.models import Competency
from django.utils import timezone
from datetime import timedelta, datetime


class Org(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='industry', null=True, blank=True)
    logo = models.FileField(upload_to='media/logo', blank=True, null=True)
    validity = models.IntegerField(default=30)  # Default validity is 30 days
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    
    def __str__(self):
        return self.name

    def disable_soon(self):
        # Checks if 3 days are left before disabling
        return self.validity <= 3

    def disable(self):
        # Disable org after validity expires
        self.is_active = False
        self.save()    

class SubOrg1(models.Model):
    def __str__(self):
        return f"{self.name} - {self.org.name}"

    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='org', null=False, blank=False, default= 7)    


class Role1(models.Model):
    def __str__(self):
        return f"{self.role_type} - {self.suborg.name} - {self.suborg.org.name}"
        #return self.role_type

    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('sub-admin', 'Sub-Admin'),
        ('admin', 'Admin'),
    ]    

    suborg = models.ForeignKey(SubOrg1, on_delete=models.CASCADE, related_name='suborgrole', null=True, blank=True)
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default = 'admin')    


class Weightage(models.Model):
    suborg = models.ForeignKey(SubOrg1, on_delete=models.CASCADE, related_name='suborg', null=True, blank=True)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE, default=1, related_name= 'rolecompetency')
    weightage = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.competency} - {self.suborg.name} - {self.weightage}'
