# proj/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bodhiguru.settings')
app = Celery('bodhiguru')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# proj/settings.py
CELERY_BEAT_SCHEDULE = {
    'check-org-validity-every-day': {
        'task': 'org.tasks.check_org_validity',
        'schedule': timedelta(days=1),
    },
}
