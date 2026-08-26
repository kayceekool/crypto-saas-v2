import pytest

from pydantic import ValidationError

from backend.api.schemas.health import (
    HealthComponent,
    HealthResponse,
)


def test_valid_health_response():

    result = HealthResponse(
        status="healthy",
        components={},
    )

    assert result.status == "healthy"
    assert result.components == {}


def test_health_component():

    result = HealthComponent(
        status="healthy",
        detail="All systems operational.",
        updated_at="2026-08-14T12:00:00+00:00",
    )

    assert result.status == "healthy"
    assert (
        result.detail
        == "All systems operational."
    )


def test_health_response_with_component():

    result = HealthResponse(
        status="healthy",
        components={
            "database": HealthComponent(
                status="healthy",
                detail="Database ready.",
                updated_at=(
                    "2026-08-14T12:00:00+00:00"
                ),
            )
        },
    )

    assert (
        result.components["database"].status
        == "healthy"
    )


def test_unexpected_health_field_is_rejected():

    with pytest.raises(
        ValidationError
    ):

        HealthResponse(
            status="healthy",
            components={},
            unexpected="bad",
        )


def test_unexpected_component_field_is_rejected():

    with pytest.raises(
        ValidationError
    ):

        HealthComponent(
            status="healthy",
            detail="OK",
            updated_at=(
                "2026-08-14T12:00:00+00:00"
            ),
            unexpected="bad",
        )


def test_health_response_serializes():

    result = HealthResponse(
        status="healthy",
        components={},
    )

    data = result.model_dump()

    assert data == {
        "status": "healthy",
        "components": {},
    }