from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi import FastAPI

from sqlalchemy.ext.asyncio import AsyncSession

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

from backend.api.schemas.execution_monitor import (
    ExecutionMonitoringSummaryResponse,
)

from backend.core.database import (
    get_db,
)

from backend.core.logging import (
    configure_logging,
    get_logger,
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

from backend.routes.system import (
    router as system_router,
)

from backend.runtime.lifecycle import (
    lifecycle,
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
# System API
# --------------------------------------------------

app.include_router(
    system_router
)


# --------------------------------------------------
# Execution monitoring API
# --------------------------------------------------
#
# Package 41 established that this endpoint must
# exist on the final FastAPI application.
#
# Keep the explicit application registration while
# the execution API remains under active development.
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

app.include_router(
    execution_monitor_router
)