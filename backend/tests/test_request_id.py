from fastapi import FastAPI, Request

from fastapi.testclient import TestClient

from backend.api.request_id import (
    REQUEST_ID_HEADER,
    get_request_id,
)


def create_app() -> FastAPI:

    application = FastAPI()

    @application.get("/request-id")
    async def request_id(
        request: Request,
    ):

        return {
            "request_id": get_request_id(
                request
            )
        }

    return application


def test_request_id_is_generated():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/request-id"
    )

    assert response.status_code == 200

    data = response.json()

    assert "request_id" in data

    assert isinstance(
        data["request_id"],
        str,
    )

    assert len(
        data["request_id"]
    ) > 0


def test_supplied_request_id_is_preserved():

    application = create_app()

    client = TestClient(
        application
    )

    supplied_id = "test-request-123"

    response = client.get(
        "/request-id",
        headers={
            REQUEST_ID_HEADER: supplied_id,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "request_id": supplied_id,
    }


def test_empty_request_id_generates_new_id():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/request-id",
        headers={
            REQUEST_ID_HEADER: "",
        },
    )

    assert response.status_code == 200

    request_id = response.json()[
        "request_id"
    ]

    assert isinstance(
        request_id,
        str,
    )

    assert len(request_id) > 0


def test_different_requests_get_different_ids():

    application = create_app()

    client = TestClient(
        application
    )

    first_response = client.get(
        "/request-id"
    )

    second_response = client.get(
        "/request-id"
    )

    assert (
        first_response.status_code
        == 200
    )

    assert (
        second_response.status_code
        == 200
    )

    first_id = first_response.json()[
        "request_id"
    ]

    second_id = second_response.json()[
        "request_id"
    ]

    assert first_id != second_id