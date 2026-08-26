import pytest

from pydantic import ValidationError

from backend.api.schemas.health import (
    HealthResponse,
)


def test_valid_health_response():

    result = HealthResponse(
        status="healthy"
    )

    assert result.status == "healthy"


def test_status_must_be_string():

    result = HealthResponse(
        status="ready"
    )

    assert isinstance(
        result.status,
        str,
    )


def test_unexpected_field_is_rejected():

    with pytest.raises(
        ValidationError
    ):

        HealthResponse(
            status="healthy",
            unexpected="bad",
        )


def test_health_response_serializes():

    result = HealthResponse(
        status="healthy"
    )

    data = result.model_dump()

    assert data == {
        "status": "healthy"
    }