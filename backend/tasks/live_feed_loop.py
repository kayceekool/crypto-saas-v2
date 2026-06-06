# backend/tasks/live_feed_loop.py

import asyncio

from services.live_feed import (
    LiveFeed
)

async def live_feed_loop():

    while True:

        try:

            await LiveFeed.update()

        except Exception as e:

            print(
                "LIVE FEED ERROR",
                e
            )

        await asyncio.sleep(15)