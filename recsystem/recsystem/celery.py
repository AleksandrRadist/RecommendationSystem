import os
from celery.schedules import crontab
from celery import Celery
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recsystem.settings')

app = Celery('recsystem')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()



app.conf.beat_schedule = {
    'create': {
        'task': 'analytics.tasks.update_recommendation_model',
        'schedule': crontab(hour=17, minute=10)
    }
}