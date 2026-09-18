import asyncio
from datetime import timedelta

from src.core.broker import broker
from src.core.config import settings
from src.core.database import async_session
from src.core.http import CryptoClient
from src.crypto.repository import add_crypto_data

INSTRUMENTS = {
    "btc": "BTC-PERPETUAL",
    "eth": "ETH-PERPETUAL",
}


@broker.task(
    task_name="fetch_crypto_prices",
    schedule=[
        {
            "interval": timedelta(seconds=settings.crypto.INTERVAL),
            "schedule_id": "fetch_crypto_prices",
        }
    ],
    retry_on_error=True,
)
async def fetch_crypto_prices() -> None:
    client = CryptoClient()
    try:
        prices = await asyncio.gather(
            *(
                client.get(f"ticker?instrument_name={instrument}")
                for instrument in INSTRUMENTS.values()
            )
        )
    finally:
        await client.session.close()

    async with async_session() as session:
        await add_crypto_data(session, dict(zip(INSTRUMENTS, prices, strict=True)))
