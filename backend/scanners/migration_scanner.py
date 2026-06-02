import asyncio

async def migration_loop():

    while True:

        try:

            print(
                "[MIGRATION] scanning..."
            )

        except Exception as e:

            print(
                "[MIGRATION ERROR]",
                e
            )

        await asyncio.sleep(30)