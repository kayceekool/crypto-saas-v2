from services.solana_client import (
    SolanaClient
)

client = SolanaClient()


async def recent_signatures(
    address,
    limit=20
):

    data = await client.rpc(
        "getSignaturesForAddress",
        [
            address,
            {"limit": limit}
        ]
    )

    return data.get(
        "result",
        []
    )