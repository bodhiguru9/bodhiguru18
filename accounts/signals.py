from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Account
from SaaS.models import SaaS, Feature

from datetime import datetime, timedelta

@receiver(post_save, sender=Account)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        SaaS.objects.create(
            user = instance,
            feature = Feature.objects.filter(name__icontains="Premium").first(),
            startdate = datetime.now(),
            enddate = datetime.now() + timedelta(days=30)
        )
