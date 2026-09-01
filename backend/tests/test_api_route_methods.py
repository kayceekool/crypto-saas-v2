from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def route_methods(path):

    methods = set()

    for route in app.routes:

        if getattr(
            route,
            "path",
            None,
        ) == path:

            methods.update(
                getattr(
                    route,
                    "methods",
                    set(),
                )
            )

    return methods


def test_root_is_get():

    assert route_methods("/") == {
        "GET"
    }


def test_health_is_get():

    assert route_methods(
        "/health"
    ) == {"GET"}


def test_ready_is_get():

    assert route_methods(
        "/ready"
    ) == {"GET"}


def test_status_is_get():

    assert route_methods(
        "/status"
    ) == {"GET"}


def test_metrics_is_get():

    assert route_methods(
        "/metrics"
    ) == {"GET"}


def test_providers_is_get():

    assert route_methods(
        "/providers"
    ) == {"GET"}


def test_execution_summary_is_get():

    assert route_methods(
        "/execution/summary"
    ) == {"GET"}