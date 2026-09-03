from backend.main import app

from backend.routes.system import (
    router as system_router,
)


def test_system_router_is_registered():

    registered_paths = {
        route.path
        for route in app.routes
        if hasattr(route, "path")
    }

    system_paths = {
        route.path
        for route in system_router.routes
        if hasattr(route, "path")
    }

    assert system_paths.issubset(
        registered_paths
    )


def test_system_root_is_registered():

    assert any(
        route.path == "/"
        and "GET" in route.methods
        for route in app.routes
    )


def test_system_health_is_registered():

    assert any(
        route.path == "/health"
        and "GET" in route.methods
        for route in app.routes
    )


def test_system_ready_is_registered():

    assert any(
        route.path == "/ready"
        and "GET" in route.methods
        for route in app.routes
    )


def test_system_status_is_registered():

    assert any(
        route.path == "/status"
        and "GET" in route.methods
        for route in app.routes
    )


def test_system_metrics_is_registered():

    assert any(
        route.path == "/metrics"
        and "GET" in route.methods
        for route in app.routes
    )


def test_system_providers_is_registered():

    assert any(
        route.path == "/providers"
        and "GET" in route.methods
        for route in app.routes
    )