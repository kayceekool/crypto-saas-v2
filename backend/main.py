from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.health import health_manager
from backend.core.logging import configure_logging, get_logger
from backend.core.metrics import metrics
from backend.core.provider_registry import provider_registry
from backend.core.settings import settings
from backend.runtime.lifecycle import lifecycle

from backend.routes.execution_monitor import (
    router as execution_monitor_router,
)

from backend.api.schemas.health import (
    HealthResponse,
)


configure_logging()

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await lifecycle.start()

    try:
        yield

    finally:
        await lifecycle.stop()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
)


# --------------------------------------------------
# Execution monitoring API
# --------------------------------------------------

app.include_router(
    execution_monitor_router
)


@app.get("/")
async def root():

    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": lifecycle.state.value,
    }


@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    return health_manager.snapshot()


@app.get("/metrics")
async def application_metrics():

    return metrics.snapshot()


@app.get("/providers")
async def providers():

    return provider_registry.snapshot()