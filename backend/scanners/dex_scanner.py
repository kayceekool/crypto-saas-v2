import httpx
from services.scoring_engine import ScoringEngine

token["score"] = ScoringEngine.calculate(
    token
)

from core.config import (
    DEXSCREENER_URL
)


class DexScanner:

    async def search(
        self,
        query
    ):

        async with httpx.AsyncClient() as client:

            r = await client.get(
                f"{DEXSCREENER_URL}?q={query}"
            )

            return r.json()