import asyncio

from celery import shared_task

from src.database.connection import create_celery_sessionmaker
from src.client.service import prepare_to_task


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10)
def task_get_crypto_currency(self):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    Session = create_celery_sessionmaker()
    try:
        loop.run_until_complete(prepare_to_task(Session))
    finally:
        loop.close()
