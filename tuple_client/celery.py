from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuple_client.settings')

app = Celery('tuple_client')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'run-scoring-daily': {
        'task': 'database_management.scheduled_tasks.scoring',
        'schedule': 10.0,
        'args': ()
    },
    'run-training-weekly': {
        'task': 'database_management.scheduled_tasks.training',
        'schedule': 10.0,
        'args': ()
    }
}

# app.conf.beat_schedule = {
#     'add-every-30-seconds': {
#         'task': 'database_management.scheduled_tasks.temporary',
#         'schedule': 5.0,
#         'args': (16, 16)
#     },
# }

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


    # @app.on_after_configure.connect
    # def setup_periodic_tasks(sender, **kwargs):
    #     sender.add_periodic_task(5.0, temporary.s(5, 7), name='add every 5 seconds')
    #
    # @app.task
    # def test(arg):
    #     print(arg)
    #     return arg