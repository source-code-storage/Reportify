"""
Celery application configuration
"""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "report_assistant",
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    include=[
        "app.worker.tasks.pdf_processing",
        "app.worker.tasks.ocr_processing",
        "app.worker.tasks.embedding_generation",
    ],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
)
