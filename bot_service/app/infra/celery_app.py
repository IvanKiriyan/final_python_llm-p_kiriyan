from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "bot-service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
)

celery_app.autodiscover_tasks(["app.tasks"])