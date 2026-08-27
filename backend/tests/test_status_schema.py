import pytest

from pydantic import ValidationError

from backend.api.schemas.status import (
    StatusResponse,
)


def valid_status():

    return {
        "name": "V3 Backend",
        "version": "3.0.0",
        "status": "healthy",
        "ready": True,
        "lifecycle": "running",
    }


def test_valid_status_response():

    result = StatusResponse(
        **valid_status()
    )

    assert result.name == "V3 Backend"

    assert result.version == "3.0.0"

    assert result.status == "healthy"

    assert result.ready is True

    assert (
        result.lifecycle
        == "running"
    )


def test_status_response_serializes():

    result = StatusResponse(
        **valid_status()
    )

    data = result.model_dump()

    assert data == valid_status()


def test_extra_field_is_rejected():

    data = valid_status()

    data["unexpected"] = "bad"

    with pytest.raises(
        ValidationError
    ):

        StatusResponse(
            **data
        )


def test_not_ready_status():

    result = StatusResponse(
        name="V3 Backend",
        version="3.0.0",
        status="starting",
        ready=False,
        lifecycle="starting",
    )

    assert result.ready is False

    assert (
        result.status
        == "starting"
    )

    assert (
        result.lifecycle
        == "starting"
    )