from backend.routes.system import (
    router,
)


def get_routes():

    return {
        route.path
        for route in router.routes
        if hasattr(route, "path")
    }


def route_methods(path):

    methods = set()

    for route in router.routes:

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


def test_system_router_exists():

    assert router is not None


def test_root_route_exists():

    assert "/" in get_routes()


def test_health_route_exists():

    assert "/health" in get_routes()


def test_ready_route_exists():

    assert "/ready" in get_routes()


def test_status_route_exists():

    assert "/status" in get_routes()


def test_metrics_route_exists():

    assert "/metrics" in get_routes()


def test_providers_route_exists():

    assert "/providers" in get_routes()


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