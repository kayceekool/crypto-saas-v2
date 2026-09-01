from backend.main import app


def test_execution_monitor_router_is_registered():

    matching_routes = [
        route
        for route in app.routes
        if getattr(
            route,
            "path",
            None,
        )
        == "/execution/summary"
    ]

    assert matching_routes, (
        "The execution monitoring router "
        "is not registered on backend.main.app"
    )


def test_execution_summary_route_has_get_method():

    matching_routes = [
        route
        for route in app.routes
        if getattr(
            route,
            "path",
            None,
        )
        == "/execution/summary"
    ]

    assert matching_routes

    route = matching_routes[0]

    assert "GET" in route.methods