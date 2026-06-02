import httpx

from core.config import (
    SOLANA_RPC_URL
)


class SolanaClient:

    async def rpc(
        self,
        method,
        params=None
    ):

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or []
        }

        async with httpx.AsyncClient() as client:

            response = await client.post(
                SOLANA_RPC_URL,
                json=payload
            )

            return response.json()