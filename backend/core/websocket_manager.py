from fastapi import WebSocket
import json


class WebSocketManager:

    def __init__(self):
        self.connections = []

    async def connect(self, websocket):

        await websocket.accept()

        self.connections.append(websocket)

    async def disconnect(self, websocket):

        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message):

        dead = []

        for ws in self.connections:

            try:
                await ws.send_text(
                    json.dumps(message)
                )

            except:

                dead.append(ws)

        for ws in dead:
            self.disconnect(ws)
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