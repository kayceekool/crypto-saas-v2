from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.cors import (
    configure_cors,
)

from backend.api.errors import (
    APIError,
    api_error_handler,
)

from backend.api.middleware import (
    RequestIDMiddleware,
)

from backend.api.schemas.health import (
    HealthResponse,
)

from backend.api.schemas.readiness import (
    ReadinessResponse,
)

from backend.api.schemas.status import (
    StatusResponse,
)

from backend.api.schemas.execution_monitor import (
    ExecutionMonitoringSummaryResponse,
)

from backend.core.database import (
    get_db,
)

from backend.core.health import (
    health_manager,
)

from backend.core.logging import (
    configure_logging,
    get_logger,
)

from backend.core.metrics import (
    metrics,
)

from backend.core.provider_registry import (
    provider_registry,
)

from backend.core.settings import (
    settings,
)

from backend.execution.monitor import (
    build_execution_summary,
)

from backend.routes.execution_monitor import (
    router as execution_monitor_router,
)

from backend.runtime.lifecycle import (
    lifecycle,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from fastapi import Depends


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
# API error handling
# --------------------------------------------------

app.add_exception_handler(
    APIError,
    api_error_handler,
)


# --------------------------------------------------
# Request identification
# --------------------------------------------------

app.add_middleware(
    RequestIDMiddleware
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

configure_cors(
    app,
    settings.cors_origins,
)


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
async def root():

    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": lifecycle.state.value,
    }


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    return health_manager.snapshot()


# --------------------------------------------------
# Readiness
# --------------------------------------------------

@app.get(
    "/ready",
    response_model=ReadinessResponse,
)
async def readiness():

    return {
        "ready": (
            lifecycle.state.value
            == "running"
        ),
        "status": lifecycle.state.value,
    }


# --------------------------------------------------
# Status
# --------------------------------------------------

@app.get(
    "/status",
    response_model=StatusResponse,
)
async def status():

    lifecycle_state = (
        lifecycle.state.value
    )

    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": (
            "healthy"
            if lifecycle_state == "running"
            else lifecycle_state
        ),
        "ready": (
            lifecycle_state == "running"
        ),
        "lifecycle": lifecycle_state,
    }


# --------------------------------------------------
# Metrics
# --------------------------------------------------

@app.get("/metrics")
async def application_metrics():

    return metrics.snapshot()


# --------------------------------------------------
# Providers
# --------------------------------------------------

@app.get("/providers")
async def providers():

    return provider_registry.snapshot()


# --------------------------------------------------
# Execution monitoring API
# --------------------------------------------------
#
# The execution-monitor router remains imported and
# defined normally.
#
# The endpoint is also registered explicitly on the
# application object. This guarantees that the final
# FastAPI application contains:
#
# GET /execution/summary
#
# --------------------------------------------------

@app.get(
    "/execution/summary",
    response_model=(
        ExecutionMonitoringSummaryResponse
    ),
)
async def execution_summary(
    db: AsyncSession = Depends(get_db),
):

    summary = await build_execution_summary(
        db
    )

    return summary.to_dict()


# --------------------------------------------------
# Execution monitoring router
# --------------------------------------------------
#
# Keep the router registration present as part of
# the application's API structure.
#
# The explicit application endpoint above guarantees
# registration on the final app object.
#
# --------------------------------------------------

app.include_router(
    execution_monitor_router
)