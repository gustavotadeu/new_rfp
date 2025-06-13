from celery import Celery
import os

default_redis = 'redis://redis:6379/0'

celery_app = Celery(
    'rfpgen',
    broker=os.getenv('CELERY_BROKER_URL', default_redis),
    backend=os.getenv('CELERY_RESULT_BACKEND', default_redis),
)

celery_app.conf.task_routes = {'backend.app.tasks.*': {'queue': 'default'}}
