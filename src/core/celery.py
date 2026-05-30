from datetime import timedelta

from celery import Celery

from src.core.config import settings

app = Celery("tasks", broker=settings.CELERY_BROKER_URL)
app.autodiscover_tasks(["src.crypto"])

app.conf.beat_schedule = {
    "get_index_price_every_minute": {
        "task": "src.crypto.tasks.task_get_crypto_currency",
        "schedule": timedelta(minutes=1),
    },
}
