from fastapi import APIRouter

from backend.api.schemas.health import (
    HealthResponse,
)

from backend.api.schemas.readiness import (
    ReadinessResponse,
)

from backend.api.schemas.status import (
    StatusResponse,
)

from backend.core.health import (
    health_manager,
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

from backend.runtime.lifecycle import (
    lifecycle,
)


router = APIRouter(
    tags=["system"],
)


@router.get("/")
async def root():

    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": lifecycle.state.value,
    }


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    return health_manager.snapshot()


@router.get(
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


@router.get(
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


@router.get("/metrics")
async def application_metrics():

    return metrics.snapshot()


@router.get("/providers")
async def providers():

    return provider_registry.snapshot()