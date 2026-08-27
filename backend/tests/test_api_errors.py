from fastapi import FastAPI

from fastapi.testclient import (
    TestClient,
)

from backend.api.errors import (
    APIError,
    api_error_handler,
)


def create_app():

    application = FastAPI()

    application.add_exception_handler(
        APIError,
        api_error_handler,
    )

    @application.get("/test-error")
    async def test_error():

        raise APIError(
            error="test_error",
            message="This is a test error.",
            status_code=418,
        )

    return application


def test_api_error_handler():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test-error"
    )

    assert response.status_code == 418

    data = response.json()

    assert (
        data["error"]
        == "test_error"
    )

    assert (
        data["message"]
        == "This is a test error."
    )


def test_api_error_payload_contains_only_contract_fields():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test-error"
    )

    data = response.json()

    assert set(data.keys()) == {
        "error",
        "message",
    }


def test_api_error_defaults_to_bad_request():

    error = APIError(
        error="invalid_request",
        message="Invalid request.",
    )

    assert (
        error.status_code
        == 400
    )

    assert (
        error.error
        == "invalid_request"
    )

    assert (
        error.message
        == "Invalid request."
    )


def test_api_error_custom_status():

    error = APIError(
        error="unavailable",
        message="Service unavailable.",
        status_code=503,
    )

    assert (
        error.status_code
        == 503
    )