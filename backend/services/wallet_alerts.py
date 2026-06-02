async def smart_wallet_alert(
    manager,
    wallet,
    token
):

    await manager.broadcast({
        "type": "smart_wallet",
        "wallet": wallet,
        "token": token
    })