from backend.api.cors import configure_cors


def test_cors_origins_are_parsed_correctly():

    origins = (
        "http://localhost:3000,"
        "https://example.vercel.app"
    )

    application = None

    # Verify the configuration function
    # accepts multiple origins without error.
    from fastapi import FastAPI

    application = FastAPI()

    configure_cors(
        application,
        origins,
    )

    assert len(
        application.user_middleware
    ) == 1


def test_cors_allows_single_configured_origin():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    application = FastAPI()

    configure_cors(
        application,
        "http://localhost:3000",
    )

    @application.get("/test")
    async def test():

        return {
            "status": "ok",
        }

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


def test_cors_rejects_unconfigured_origin():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    application = FastAPI()

    configure_cors(
        application,
        "http://localhost:3000",
    )

    @application.get("/test")
    async def test():

        return {
            "status": "ok",
        }

    client = TestClient(
        application
    )

    response = client.get(
        "/test",
        headers={
            "Origin":
                "https://unknown.example",
        },
    )

    assert response.status_code == 200

    assert (
        "access-control-allow-origin"
        not in response.headers
    )


def test_cors_empty_configuration_is_safe():

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    application = FastAPI()

    configure_cors(
        application,
        "",
    )

    @application.get("/test")
    async def test():

        return {
            "status": "ok",
        }

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