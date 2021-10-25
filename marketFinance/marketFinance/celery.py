import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','marketFinance.settings')

app = Celery('marketFinance')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_coins_data_20s': {
        'task': 'coinMarket.tasks.get_coins_data',
        'schedule': 30.0
    }
}

app.autodiscover_tasks()