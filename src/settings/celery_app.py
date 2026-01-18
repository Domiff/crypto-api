from datetime import timedelta

from celery import Celery


app = Celery("tasks")
app.autodiscover_tasks(["src.client"])


app.conf.beat_schedule = {
    "get_index_price_every_minute": {
        "task": "src.client.tasks.task_get_crypto_currency",
        "schedule": timedelta(minutes=1),
    },
}
