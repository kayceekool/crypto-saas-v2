from fastapi.testclient import TestClient

from backend.main import app

from backend.core.settings import settings


def test_main_application_has_cors_middleware():

    middleware_names = [
        middleware.cls.__name__
        for middleware
        in app.user_middleware
    ]

    assert (
        "CORSMiddleware"
        in middleware_names
    )


def test_main_application_has_request_id_middleware():

    middleware_names = [
        middleware.cls.__name__
        for middleware
        in app.user_middleware
    ]

    assert (
        "RequestIDMiddleware"
        in middleware_names
    )


def test_main_application_accepts_configured_origin():

    client = TestClient(app)

    origin = (
        settings.cors_origins
        .split(",")[0]
        .strip()
    )

    if not origin:
        origin = (
            "http://localhost:3000"
        )

    response = client.get(
        "/",
        headers={
            "Origin": origin,
        },
    )

    assert response.status_code == 200

    assert (
        response.headers.get(
            "access-control-allow-origin"
        )
        == origin
        or settings.cors_origins
        == "*"
    )


def test_main_application_returns_request_id():

    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200

    assert (
        "X-Request-ID"
        in response.headers
    )

    request_id = response.headers[
        "X-Request-ID"
    ]

    assert isinstance(
        request_id,
        str,
    )

    assert len(request_id) > 0