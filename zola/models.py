from django.db import models

from competency.models import Competency
from orgss.models import Role
from accounts.models import Account

class Item(models.Model):
    def __str__(self):
        return self.item_name

    Gender_CHOICES = [
        ("female", "Female"),
        ("male", "Male"),
        ("all", "All"),
    ]
    
    Type_CHOICES = [
        ("simulation", "Simulation"),
        ("email", "Email")
    ]
    
    Scenario_Type_CHOICES = [
        ("sales", "Sales"),
        ("customer_service", "Customer Service"),
        ("interview", "Interview"),
    ]

    item_name = models.CharField(max_length=700)
    item_description = models.CharField(max_length=300, blank=True, null = True)
    item_video = models.URLField(null=True, blank=True)
    item_background = models.FileField(upload_to='media/item/item_background', null=True, blank=True)
    item_answer = models.TextField(null=True, blank=True)
    item_emotion = models.TextField(null=True, blank=True)
    item_answercount = models.IntegerField(default=0)
    category = models.CharField(max_length=256, blank=True, default="Personal")
    thumbnail = models.FileField(upload_to='media/item/thumbnail', null=True, blank=True)  
    item_gender = models.CharField(max_length=30, choices=Gender_CHOICES, default="all")
    item_type = models.CharField(max_length=30, choices=Type_CHOICES, default="simulation")
    scenario_type = models.CharField(max_length= 30, choices=Scenario_Type_CHOICES, default="sales")
    coming_across_as = models.CharField(max_length=250, null=True, blank=True)
    competencys = models.ManyToManyField(Competency, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='seanrole', null=True, blank=True)
    level = models.IntegerField(default=1)
    expert = models.URLField(blank = True, null=True)
    is_approved = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)

    def get_competencys_as_string(self):
        return ', '.join(self.competencys.values_list('competency_name', flat=True))

class ItemResult(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at} - {self.score}"

class Suggestion(models.Model):
    def __str__(self):
        return self.suggestion_text

    name = models.CharField(max_length=256)
    suggestion_text = models.TextField()
