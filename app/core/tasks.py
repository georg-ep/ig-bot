from celery import shared_task
from celery.signals import worker_init, worker_shutdown

from core.redis import redis_storage


@worker_init.connect
def on_worker_init(*_, **__):
    keys = redis_storage.connection.keys("running_tasks:*")

    if keys:
        redis_storage.connection.delete(*keys)


@worker_shutdown.connect
def on_worker_shutdown(*_, **__):
    redis_storage.connection.close()
