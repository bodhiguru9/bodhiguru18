from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Account, UserProfile

from datetime import datetime, timedelta

from django.utils import timezone


@receiver(post_save, sender=Account)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        SaaS.objects.create(
            user = instance,
            feature = Feature.objects.filter(name__icontains="Premium").first(),
            startdate = datetime.now(),
            enddate = datetime.now() + timedelta(days=30)
        )

@receiver(post_save, sender=Account)
def deactivate_user_after_validity(sender, instance, **kwargs):
    if instance.validity < timezone.now():
        instance.is_active = False
        instance.save()
        user_profile = UserProfile.objects.get(account=instance)
        user_profile.is_active = False
        user_profile.save()