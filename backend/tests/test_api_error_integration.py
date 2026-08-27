from fastapi import FastAPI

from fastapi.testclient import TestClient

from backend.api.errors import (
    APIError,
    api_error_handler,
)


def create_test_app():

    application = FastAPI()

    application.add_exception_handler(
        APIError,
        api_error_handler,
    )

    @application.get("/test-error")
    async def test_error():

        raise APIError(
            error="integration_error",
            message="Integration test error.",
            status_code=503,
        )

    @application.get("/normal")
    async def normal():

        return {
            "status": "ok",
        }

    return application


def test_api_error_integration():

    application = create_test_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test-error"
    )

    assert response.status_code == 503

    data = response.json()

    assert data == {
        "error": "integration_error",
        "message": "Integration test error.",
    }


def test_normal_endpoint_is_unaffected():

    application = create_test_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/normal"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
    }


def test_api_error_status_code_is_preserved():

    application = create_test_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test-error"
    )

    assert (
        response.status_code
        == 503
    )


def test_error_response_content_type():

    application = create_test_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test-error"
    )

    assert (
        response.headers[
            "content-type"
        ].startswith(
            "application/json"
        )
    )