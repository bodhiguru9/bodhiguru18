# org/management/commands/disable_orgs.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from orgss.models import Org

class Command(BaseCommand):
    help = 'Disable orgs after their validity period and notify admin'

    def handle(self, *args, **kwargs):
        orgs = Org.objects.filter(is_active=True)
        for org in orgs:
            if org.validity <= 0:
                # Disable org
                org.disable()
                # Disable all users under that org
                org.users.update(is_active=False)
            elif org.disable_soon:
                # Notify admin if 3 days remain before disabling
                send_mail(
                    'Org Disabling Soon',
                    f'The org {org.name} will be disabled in 3 days.',
                    'admin@yourapp.com',
                    ['arindam@bodhiguru.com'],
                    fail_silently=False,
                )
