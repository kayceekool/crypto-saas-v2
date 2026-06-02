from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):

        self.connections = []

    async def connect(
        self,
        websocket: WebSocket
    ):

        await websocket.accept()

        self.connections.append(
            websocket
        )

    def disconnect(
        self,
        websocket
    ):

        self.connections.remove(
            websocket
        )

    async def broadcast(
        self,
        data
    ):

        for connection in self.connections:

            try:

                await connection.send_json(
                    data
                )

            except:

                pass


manager = ConnectionManager()