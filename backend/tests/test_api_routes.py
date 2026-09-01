from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def get_routes():

    return {
        route.path
        for route in app.routes
        if hasattr(route, "path")
    }


def test_root_route_exists():

    routes = get_routes()

    assert "/" in routes


def test_health_route_exists():

    routes = get_routes()

    assert "/health" in routes


def test_readiness_route_exists():

    routes = get_routes()

    assert "/ready" in routes


def test_status_route_exists():

    routes = get_routes()

    assert "/status" in routes


def test_metrics_route_exists():

    routes = get_routes()

    assert "/metrics" in routes


def test_providers_route_exists():

    routes = get_routes()

    assert "/providers" in routes


def test_execution_summary_route_exists():

    routes = get_routes()

    assert (
        "/execution/summary"
        in routes
    )


def test_root_route_responds():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "name" in data

    assert "version" in data

    assert "status" in data


def test_request_id_is_present_on_root():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        "X-Request-ID"
        in response.headers
    )

    assert (
        len(
            response.headers[
                "X-Request-ID"
            ]
        )
        > 0
    )