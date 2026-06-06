class AlertEngine:

    subscribers = set()

    @classmethod
    async def broadcast(
        cls,
        message
    ):

        dead = []

        for ws in cls.subscribers:

            try:

                await ws.send_json(
                    message
                )

            except:

                dead.append(
                    ws
                )

        for ws in dead:

            cls.subscribers.discard(
                ws
            )