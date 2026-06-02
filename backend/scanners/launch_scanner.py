import asyncio

async def launch_loop():

    while True:

        try:

            print(
                "[LAUNCH] scanning..."
            )

        except Exception as e:

            print(
                "[LAUNCH ERROR]",
                e
            )

        await asyncio.sleep(20)