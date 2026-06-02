import asyncio

async def wallet_loop():

    while True:

        try:

            print(
                "[WALLET] scanning..."
            )

        except Exception as e:

            print(
                "[WALLET ERROR]",
                e
            )

        await asyncio.sleep(45)