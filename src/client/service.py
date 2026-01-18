from src.client.crypto_client import CryptoClient
from src.client.urls import urls
from src.database.models import Btc, Eth


async def get_crypto_currency():
    async with CryptoClient(base_url=urls.get("base")) as session:
        btc = await session.get(urls.get("btc"))
        eth = await session.get(urls.get("eth"))
        return btc, eth


async def add_to_database(btc_data: dict, eth_data: dict, session):
    async with session() as session:
        btc = Btc(
            index_price=btc_data.get("index_price"),
            instrument_name=btc_data.get("instrument_name"),
            timestamp=btc_data.get("timestamp"),
        )
        eth = Eth(
            index_price=eth_data.get("index_price"),
            instrument_name=eth_data.get("instrument_name"),
            timestamp=eth_data.get("timestamp"),
        )
        session.add(btc)
        session.add(eth)
        await session.commit()


async def prepare_to_task(session):
    btc, eth = await get_crypto_currency()
    await add_to_database(btc, eth, session)
