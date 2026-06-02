import asyncio

from services.wallet_discovery import (
    get_wallets
)

async def live_wallet_loop():

    while True:

        wallets = get_wallets()

        print(
            f"[WALLETS] {len(wallets)} tracked"
        )

        await asyncio.sleep(30)