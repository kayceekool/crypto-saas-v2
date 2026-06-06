from services.alert_engine import (
    AlertEngine
)

async def register_dashboard(
    websocket
):

    AlertEngine.subscribers.add(
        websocket
    )