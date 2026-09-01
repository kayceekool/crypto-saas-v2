from fastapi import FastAPI

from fastapi.testclient import (
    TestClient,
)

from backend.api.cors import (
    configure_cors,
)


def create_app(
    origins="http://localhost:3000",
):

    application = FastAPI()

    configure_cors(
        application,
        origins,
    )

    @application.get("/test")
    async def test_endpoint():

        return {
            "status": "ok",
        }

    return application


def test_allowed_origin():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test",
        headers={
            "Origin":
                "http://localhost:3000",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "access-control-allow-origin"
        ]
        == "http://localhost:3000"
    )


def test_disallowed_origin():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test",
        headers={
            "Origin":
                "http://evil.example",
        },
    )

    assert response.status_code == 200

    assert (
        "access-control-allow-origin"
        not in response.headers
    )


def test_multiple_origins():

    application = create_app(
        "http://localhost:3000,"
        "https://example.vercel.app"
    )

    client = TestClient(
        application
    )

    response = client.get(
        "/test",
        headers={
            "Origin":
                "https://example.vercel.app",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "access-control-allow-origin"
        ]
        == "https://example.vercel.app"
    )


def test_empty_origin_configuration_uses_wildcard():

    application = create_app("")

    client = TestClient(
        application
    )

    response = client.get(
        "/test",
        headers={
            "Origin":
                "http://localhost:3000",
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            "access-control-allow-origin"
        ]
        == "*"
    )