import aiohttp

from src.core.config import settings


class CryptoClient:
    def __init__(self):
        self.session = aiohttp.ClientSession(base_url=settings.crypto.URL)
    
    async def get(self, url: str) -> dict:
        async with self.session.get(url) as response:
            data = await response.json()
            result = data["result"]
            return {
                "index_price": result["index_price"],
                "instrument_name": result["instrument_name"],
            }


http = CryptoClient()
