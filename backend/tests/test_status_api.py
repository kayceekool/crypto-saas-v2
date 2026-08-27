from fastapi import FastAPI

from fastapi.testclient import (
    TestClient,
)


def create_app():

    application = FastAPI()

    @application.get(
        "/status"
    )
    async def status():

        return {
            "name": "V3 Backend",
            "version": "3.0.0",
            "status": "healthy",
            "ready": True,
            "lifecycle": "running",
        }

    return application


def test_status_endpoint():

    application = create_app()

    client = TestClient(
        application
    )

    response = client.get(
        "/status"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["name"]
        == "V3 Backend"
    )

    assert (
        data["version"]
        == "3.0.0"
    )

    assert (
        data["status"]
        == "healthy"
    )

    assert data["ready"] is True

    assert (
        data["lifecycle"]
        == "running"
    )


def test_status_contains_required_fields():

    application = create_app()

    client = TestClient(
        application
    )

    data = client.get(
        "/status"
    ).json()

    required = {
        "name",
        "version",
        "status",
        "ready",
        "lifecycle",
    }

    assert required.issubset(
        data.keys()
    )