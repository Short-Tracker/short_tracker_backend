import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'short_tracker.settings')


app = Celery('short_tracker')
app.config_from_object('django.conf:settings',
                       namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-messages': {
        'task': 'message.tasks.delete_solved_queries',
        'schedule': crontab(),
    },
}
app.conf.timezone = 'UTC'
