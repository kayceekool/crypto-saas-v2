class AlertEngine:

    subscribers = []

    @classmethod
    async def broadcast(
        cls,
        message
    ):

        for ws in cls.subscribers:

            try:

                await ws.send_json(
                    message
                )

            except:

                pass