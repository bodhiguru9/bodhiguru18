# org/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Org
from accounts.models import Account
from datetime import timedelta
from django.core.mail import send_mail

@shared_task
def check_org_validity():
    orgs = Org.objects.filter(is_active=True)
    for org in orgs:
        expiry_date = org.created_at + timedelta(days=org.validity)
        warning_date = expiry_date - timedelta(days=3)

        if timezone.now() > expiry_date:
            # Disable organization and related users
            org.is_active = False
            org.save()
            Account.objects.filter(org=org).update(is_active=False)

        elif timezone.now() > warning_date:
            # Send warning email to admin
            send_mail(
                'Organization Expiry Warning',
                'The organization {} is about to expire.'.format(org.name),
                'from@example.com',
                ['arindam@bodhiguru.com'],
                fail_silently=False,
            )
