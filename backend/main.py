from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from websocket.routes import router as ws_router
from services.alert_service import send_alert

from core.database import Base
from core.database import engine

from core.scheduler import start_scheduler

# NEW
import asyncio

# NEW
from tasks.live_feed_loop import (
    live_feed_loop
)

# NEW
from services.live_feed import (
    LiveFeed
)

app = FastAPI(
    title="Solana Intelligence Platform V2"
)

app.include_router(ws_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():

    # Existing scheduler
    await start_scheduler()

    # NEW live intelligence feed
    asyncio.create_task(
        live_feed_loop()
    )

@app.get("/")
async def root():

    return {
        "status": "online",
        "engine": "SOLANA INTELLIGENCE PLATFORM V2"
    }

@app.get("/test-alert")
async def test_alert():

    await send_alert(
        "SUPERNOVA",
        "Test Signal",
        "System operational"
    )

    return {
        "success": True
    }

# NEW
@app.get("/rankings")
async def rankings():

    return await (
        LiveFeed.update()
    )

# NEW
@app.get("/top")
async def top():

    data = await (
        LiveFeed.update()
    )

    if data:
        return data[0]

    return {}