from pathlib import Path

import backend.main as main_module


def test_main_contains_execution_router_registration():

    main_file = Path(main_module.__file__)

    source = main_file.read_text(
        encoding="utf-8"
    )

    assert (
        "app.include_router("
        in source
    )

    assert (
        "execution_monitor_router"
        in source
    )


def test_execution_router_registration_is_executed():

    routes = {
        getattr(route, "path", None)
        for route in main_module.app.routes
    }

    assert (
        "/execution/summary"
        in routes
    )


def test_execution_router_is_attached_to_same_app():

    matching_routes = [
        route
        for route in main_module.app.routes
        if getattr(
            route,
            "path",
            None,
        ) == "/execution/summary"
    ]

    assert matching_routes

    route = matching_routes[0]

    assert "GET" in route.methods