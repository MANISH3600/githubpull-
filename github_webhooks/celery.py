# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'github_webhooks.settings')


app = Celery('github_webhooks')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-pull-request-notifications-every-minute': {
        'task': 'webhook_manager.tasks.send_pull_request_notifications',
        'schedule': 40.0,  # Runs every minute
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
