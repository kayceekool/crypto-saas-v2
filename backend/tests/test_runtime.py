import pytest

from backend.core.health import (
    HealthManager,
)

from backend.core.provider_registry import (
    ProviderRegistry,
)


def test_provider_registry():

    registry = ProviderRegistry()

    registry.register(
        "Example",
        object(),
        priority=10,
    )

    snapshot = registry.snapshot()

    assert (
        snapshot["providers"][0]["name"]
        == "Example"
    )

    assert (
        snapshot["providers"][0]["priority"]
        == 10
    )


def test_health_manager():

    health = HealthManager()

    health.set_status(
        "database",
        "up",
        "ok",
    )

    snapshot = health.snapshot()

    assert (
        snapshot["status"]
        == "healthy"
    )

    assert (
        snapshot["components"]
        ["database"]
        ["status"]
        == "up"
    )


@pytest.mark.asyncio
async def test_application_import():

    from backend.main import app

    assert (
        app.title
        == "Solana Intelligence Platform V3"
    )