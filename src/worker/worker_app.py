from celery import Celery

from src.core.settings import settings

celery_app = Celery(
    'worker_app',
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BROKER_URL,
)

celery_app.autodiscover_tasks(['src.worker.tasks'])
