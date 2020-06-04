import os
from celery.schedules import crontab
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'when.settings')

app = Celery('when')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-due-every-day': {
        'task': 'tasks.initiate_due_notifications_for_all_deltas',
        'schedule': crontab(minute=45),
        'args': (16, 16),
    },
}
