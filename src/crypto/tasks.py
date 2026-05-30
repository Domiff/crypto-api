import asyncio

from celery import shared_task

from src.core.config import settings
from src.core.database import create_celery_sessionmaker
from src.core.http_client import CryptoClient
from src.crypto.repository import add_crypto_data


async def _fetch_and_save(session) -> None:
    async with CryptoClient(base_url=settings.BASE_URL) as client:
        btc = await client.get(settings.BTC)
        eth = await client.get(settings.ETH)
    await add_crypto_data(btc, eth, session)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10)
def task_get_crypto_currency(self):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    session = create_celery_sessionmaker()
    try:
        loop.run_until_complete(_fetch_and_save(session))
    finally:
        loop.close()
