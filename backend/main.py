from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from websocket.routes import router as ws_router
from services.alert_service import send_alert

app.include_router(ws_router)

from core.database import Base
from core.database import engine

from core.scheduler import start_scheduler

app = FastAPI(
    title="Solana Intelligence Platform V2"
)

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

    await start_scheduler()

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