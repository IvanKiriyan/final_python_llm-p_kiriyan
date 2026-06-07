from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "bot-service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.llm_tasks"],
)