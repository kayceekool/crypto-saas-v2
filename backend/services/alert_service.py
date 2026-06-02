from core.websocket_manager import manager


async def send_alert(
    level,
    title,
    message
):

    payload = {
        "level": level,
        "title": title,
        "message": message
    }

    await manager.broadcast(
        payload
    )