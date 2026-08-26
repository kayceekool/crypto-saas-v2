import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import Base

from backend.storage.execution_audit_db import (
    save_execution_audit,
)

from backend.storage.execution_audit_queries import (
    count_audits,
    list_by_decision,
    list_by_execution_state,
    list_by_gate_status,
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


async def add_record(
    db,
    *,
    decision,
    approved,
    executed=False,
    dry_run=True,
):

    return await save_execution_audit(
        db,
        decision=decision,
        score=700,
        confidence=65,
        risk=40,
        gate_approved=approved,
        execution_enabled=approved,
        executed=executed,
        dry_run=dry_run,
        message="Query test.",
    )


@pytest.mark.asyncio
async def test_list_by_decision(
    db,
):

    await add_record(
        db,
        decision="WATCH",
        approved=False,
    )

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
    )

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
    )

    records = await list_by_decision(
        db,
        "ACCEPT",
    )

    assert len(records) == 2

    assert all(
        record.decision
        == "ACCEPT"
        for record in records
    )


@pytest.mark.asyncio
async def test_list_by_decision_limit(
    db,
):

    for _ in range(5):

        await add_record(
            db,
            decision="ACCEPT",
            approved=True,
        )

    records = await list_by_decision(
        db,
        "ACCEPT",
        limit=2,
    )

    assert len(records) == 2


@pytest.mark.asyncio
async def test_list_by_decision_zero_limit(
    db,
):

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
    )

    records = await list_by_decision(
        db,
        "ACCEPT",
        limit=0,
    )

    assert records == []


@pytest.mark.asyncio
async def test_list_by_execution_state(
    db,
):

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
        executed=False,
        dry_run=True,
    )

    await add_record(
        db,
        decision="WATCH",
        approved=False,
        executed=False,
        dry_run=True,
    )

    records = (
        await list_by_execution_state(
            db,
            executed=False,
            dry_run=True,
        )
    )

    assert len(records) == 2


@pytest.mark.asyncio
async def test_list_by_execution_state_without_filters(
    db,
):

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
    )

    await add_record(
        db,
        decision="REJECT",
        approved=False,
    )

    records = (
        await list_by_execution_state(
            db
        )
    )

    assert len(records) == 2


@pytest.mark.asyncio
async def test_list_by_gate_status_approved(
    db,
):

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
    )

    await add_record(
        db,
        decision="WATCH",
        approved=False,
    )

    records = (
        await list_by_gate_status(
            db,
            approved=True,
        )
    )

    assert len(records) == 1

    assert (
        records[0].decision
        == "ACCEPT"
    )


@pytest.mark.asyncio
async def test_list_by_gate_status_blocked(
    db,
):

    await add_record(
        db,
        decision="REJECT",
        approved=False,
    )

    records = (
        await list_by_gate_status(
            db,
            approved=False,
        )
    )

    assert len(records) == 1

    assert (
        records[0].decision
        == "REJECT"
    )


@pytest.mark.asyncio
async def test_count_audits(
    db,
):

    assert (
        await count_audits(db)
        == 0
    )

    await add_record(
        db,
        decision="WATCH",
        approved=False,
    )

    await add_record(
        db,
        decision="ACCEPT",
        approved=True,
    )

    await add_record(
        db,
        decision="STRONG",
        approved=True,
    )

    assert (
        await count_audits(db)
        == 3
    )


@pytest.mark.asyncio
async def test_queries_preserve_dry_run_safety(
    db,
):

    await add_record(
        db,
        decision="STRONG",
        approved=True,
        executed=False,
        dry_run=True,
    )

    records = (
        await list_by_execution_state(
            db,
            executed=False,
            dry_run=True,
        )
    )

    assert len(records) == 1

    assert (
        records[0].executed
        is False
    )

    assert (
        records[0].dry_run
        is True
    )