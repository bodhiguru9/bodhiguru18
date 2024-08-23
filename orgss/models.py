from django.db import models

from industry.models import Industry
from competency.models import Competency

class Org(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='industry', null=True, blank=True)
    logo = models.FileField(upload_to='media/logo', blank=True, null=True)
    
    def __str__(self):
        return self.name

class SubOrg(models.Model):
    def __str__(self):
        return f"{self.name} - {self.org.name}"

    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500, blank=True, null=True)
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name='org', null=True, blank=True)

class Role(models.Model):
    def __str__(self):
        return f"{self.name} - {self.suborg.name} - {self.suborg.org.name}"

    name = models.CharField(max_length=250)
    suborg = models.ForeignKey(SubOrg, on_delete=models.CASCADE, related_name='suborgrole', null=True, blank=True)

class Weightage(models.Model):
    suborg = models.ForeignKey(SubOrg, on_delete=models.CASCADE, related_name='suborg', null=True, blank=True)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE, default=1, related_name= 'rolecompetency')
    weightage = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.competency} - {self.suborg.name} - {self.weightage}'
