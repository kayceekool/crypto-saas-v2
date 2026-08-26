import pytest
import pytest_asyncio

from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import (
    Base,
    get_db,
)

from backend.routes.execution_monitor import (
    router,
)

from backend.storage.execution_audit_db import (
    save_execution_audit,
)


@pytest_asyncio.fixture
async def db():

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        future=True,
    )

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )

    session_factory = (
        async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    )

    async with session_factory() as session:

        yield session

    await engine.dispose()


@pytest.fixture
def app(db):

    application = FastAPI()

    application.include_router(
        router
    )

    async def override_db():

        yield db

    application.dependency_overrides[
        get_db
    ] = override_db

    return application


@pytest.fixture
def client(app):

    return TestClient(app)


@pytest.mark.asyncio
async def test_summary_endpoint_empty_database(
    client,
):

    response = client.get(
        "/execution/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 0
    assert data["accepted"] == 0
    assert data["rejected"] == 0
    assert data["watched"] == 0
    assert data["strong"] == 0
    assert data["gate_approved"] == 0
    assert data["gate_blocked"] == 0
    assert data["executed"] == 0
    assert data["dry_run"] == 0

    assert (
        data["acceptance_rate"]
        == 0.0
    )

    assert (
        data["execution_rate"]
        == 0.0
    )

    assert (
        data["dry_run_rate"]
        == 0.0
    )


@pytest.mark.asyncio
async def test_summary_endpoint_returns_database_data(
    db,
    client,
):

    await save_execution_audit(
        db,
        decision="ACCEPT",
        score=700,
        confidence=65,
        risk=40,
        gate_approved=True,
        execution_enabled=True,
        executed=False,
        dry_run=True,
        message="Accepted.",
    )

    await save_execution_audit(
        db,
        decision="STRONG",
        score=850,
        confidence=80,
        risk=20,
        gate_approved=True,
        execution_enabled=True,
        executed=False,
        dry_run=True,
        message="Strong signal.",
    )

    await save_execution_audit(
        db,
        decision="REJECT",
        score=300,
        confidence=20,
        risk=90,
        gate_approved=False,
        execution_enabled=True,
        executed=False,
        dry_run=True,
        message="Rejected.",
    )

    response = client.get(
        "/execution/summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["accepted"] == 1
    assert data["strong"] == 1
    assert data["rejected"] == 1

    assert data["gate_approved"] == 2
    assert data["gate_blocked"] == 1

    assert data["executed"] == 0
    assert data["dry_run"] == 3

    assert (
        data["acceptance_rate"]
        == 2 / 3
    )

    assert (
        data["execution_rate"]
        == 0.0
    )

    assert (
        data["dry_run_rate"]
        == 1.0
    )


def test_summary_endpoint_is_read_only(
    client,
):

    response = client.get(
        "/execution/summary"
    )

    assert response.status_code == 200

    assert response.json()[
        "executed"
    ] == 0