import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                       'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace= 'CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'new message': {
        'task': 'NewsPaper.tasks.new_mess',
        'schedule': 30,
        'args': ("some_arg"),
    },
}

app.conf.beat_schedule ={
    'weekly_news_every_mon_8am':{
        'task': 'NewsPaper.tasks.weekly_news_report',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    }
}