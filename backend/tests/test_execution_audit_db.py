import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import Base

from backend.models.execution_audit import (
    ExecutionAudit,
)

from backend.storage.execution_audit_db import (
    list_recent_execution_audits,
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


@pytest.mark.asyncio
async def test_save_execution_audit(
    db,
):

    record = await save_execution_audit(
        db,
        decision="ACCEPT",
        score=700,
        confidence=65,
        risk=40,
        gate_approved=True,
        execution_enabled=True,
        executed=False,
        dry_run=True,
        message="Dry-run approved.",
    )

    assert record.id is not None
    assert record.decision == "ACCEPT"
    assert record.score == 700.0
    assert record.confidence == 65.0
    assert record.risk == 40.0

    assert (
        record.gate_approved
        is True
    )

    assert (
        record.execution_enabled
        is True
    )

    assert (
        record.executed
        is False
    )

    assert (
        record.dry_run
        is True
    )


@pytest.mark.asyncio
async def test_save_blocked_execution(
    db,
):

    record = await save_execution_audit(
        db,
        decision="REJECT",
        score=300,
        confidence=20,
        risk=90,
        gate_approved=False,
        execution_enabled=True,
        executed=False,
        dry_run=True,
        message="Blocked by risk gate.",
    )

    assert (
        record.gate_approved
        is False
    )

    assert (
        record.executed
        is False
    )

    assert (
        record.dry_run
        is True
    )


@pytest.mark.asyncio
async def test_list_recent_execution_audits(
    db,
):

    await save_execution_audit(
        db,
        decision="WATCH",
        score=500,
        confidence=40,
        risk=70,
        gate_approved=False,
        execution_enabled=True,
        executed=False,
        dry_run=True,
        message="Blocked.",
    )

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
        message="Approved.",
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=10,
        )
    )

    assert len(records) == 2

    assert (
        records[0].decision
        == "ACCEPT"
    )

    assert (
        records[1].decision
        == "WATCH"
    )


@pytest.mark.asyncio
async def test_recent_limit_is_safe(
    db,
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
        message="Test.",
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=0,
        )
    )

    assert records == []


@pytest.mark.asyncio
async def test_multiple_audits_are_persisted(
    db,
):

    for decision in (
        "WATCH",
        "ACCEPT",
        "STRONG",
    ):

        await save_execution_audit(
            db,
            decision=decision,
            score=700,
            confidence=65,
            risk=40,
            gate_approved=(
                decision != "WATCH"
            ),
            execution_enabled=True,
            executed=False,
            dry_run=True,
            message="Test.",
        )

    records = (
        await list_recent_execution_audits(
            db,
            limit=10,
        )
    )

    assert len(records) == 3

    assert [
        record.decision
        for record in records
    ] == [
        "STRONG",
        "ACCEPT",
        "WATCH",
    ]


def test_execution_audit_model_has_primary_key():

    primary_keys = (
        ExecutionAudit.__table__
        .primary_key
        .columns
    )

    assert len(primary_keys) == 1

    assert (
        list(primary_keys)[0].name
        == "id"
    )


def test_execution_audit_model_is_dry_run_capable():

    columns = (
        ExecutionAudit.__table__
        .columns
    )

    assert (
        "executed"
        in columns
    )

    assert (
        "dry_run"
        in columns
    )

    assert (
        "gate_approved"
        in columns
    )