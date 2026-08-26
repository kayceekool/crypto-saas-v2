from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.api.schemas.readiness import (
    ReadinessResponse,
)


def create_app():

    application = FastAPI()

    @application.get(
        "/ready",
        response_model=ReadinessResponse,
    )
    async def readiness():

        return {
            "ready": True,
            "status": "running",
        }

    return application


def test_ready_response():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/ready"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ready"] is True
    assert data["status"] == "running"


def test_readiness_schema():

    result = ReadinessResponse(
        ready=True,
        status="running",
    )

    assert result.ready is True
    assert result.status == "running"


def test_readiness_schema_rejects_extra_field():

    from pydantic import ValidationError

    try:

        ReadinessResponse(
            ready=True,
            status="running",
            unexpected="bad",
        )

    except ValidationError:

        pass

    else:

        raise AssertionError(
            "Extra fields should be rejected."
        )


def test_not_ready_state():

    result = ReadinessResponse(
        ready=False,
        status="starting",
    )

    assert result.ready is False
    assert result.status == "starting"