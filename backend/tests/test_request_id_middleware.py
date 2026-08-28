from fastapi import FastAPI

from fastapi.testclient import (
    TestClient,
)

from backend.api.middleware import (
    RequestIDMiddleware,
)

from backend.api.request_id import (
    REQUEST_ID_HEADER,
)


def create_app():

    application = FastAPI()

    application.add_middleware(
        RequestIDMiddleware
    )

    @application.get("/test")
    async def test_endpoint():

        return {
            "status": "ok",
        }

    return application


def test_request_id_header_is_returned():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test"
    )

    assert response.status_code == 200

    assert (
        REQUEST_ID_HEADER
        in response.headers
    )

    request_id = response.headers[
        REQUEST_ID_HEADER
    ]

    assert isinstance(
        request_id,
        str,
    )

    assert len(request_id) > 0


def test_supplied_request_id_is_preserved():

    application = create_app()

    client = TestClient(
        application
    )

    supplied_id = (
        "client-request-456"
    )

    response = client.get(
        "/test",
        headers={
            REQUEST_ID_HEADER:
                supplied_id
        },
    )

    assert response.status_code == 200

    assert (
        response.headers[
            REQUEST_ID_HEADER
        ]
        == supplied_id
    )


def test_each_request_gets_unique_id():

    application = create_app()

    client = TestClient(
        application
    )

    first = client.get(
        "/test"
    )

    second = client.get(
        "/test"
    )

    first_id = first.headers[
        REQUEST_ID_HEADER
    ]

    second_id = second.headers[
        REQUEST_ID_HEADER
    ]

    assert first_id != second_id


def test_normal_response_is_unchanged():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/test"
    )

    assert response.json() == {
        "status": "ok",
    }