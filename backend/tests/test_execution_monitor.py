import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import Base

from backend.execution.monitor import (
    ExecutionMonitoringSummary,
    build_execution_summary,
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
        message="Monitoring test.",
    )


@pytest.mark.asyncio
async def test_empty_summary(
    db,
):

    summary = (
        await build_execution_summary(
            db
        )
    )

    assert summary.total == 0
    assert summary.accepted == 0
    assert summary.rejected == 0
    assert summary.watched == 0
    assert summary.strong == 0
    assert summary.gate_approved == 0
    assert summary.gate_blocked == 0
    assert summary.executed == 0
    assert summary.dry_run == 0

    assert (
        summary.acceptance_rate
        == 0.0
    )

    assert (
        summary.execution_rate
        == 0.0
    )

    assert (
        summary.dry_run_rate
        == 0.0
    )


@pytest.mark.asyncio
async def test_summary_counts_decisions(
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

    await add_record(
        db,
        decision="STRONG",
        approved=True,
    )

    await add_record(
        db,
        decision="REJECT",
        approved=False,
    )

    summary = (
        await build_execution_summary(
            db
        )
    )

    assert summary.total == 5
    assert summary.watched == 1
    assert summary.accepted == 2
    assert summary.strong == 1
    assert summary.rejected == 1


@pytest.mark.asyncio
async def test_summary_counts_gate_results(
    db,
):

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

    await add_record(
        db,
        decision="WATCH",
        approved=False,
    )

    await add_record(
        db,
        decision="REJECT",
        approved=False,
    )

    summary = (
        await build_execution_summary(
            db
        )
    )

    assert (
        summary.gate_approved
        == 2
    )

    assert (
        summary.gate_blocked
        == 2
    )


@pytest.mark.asyncio
async def test_summary_counts_execution_state(
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
        decision="STRONG",
        approved=True,
        executed=False,
        dry_run=True,
    )

    summary = (
        await build_execution_summary(
            db
        )
    )

    assert summary.executed == 0
    assert summary.dry_run == 2


@pytest.mark.asyncio
async def test_summary_rates(
    db,
):

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

    await add_record(
        db,
        decision="WATCH",
        approved=False,
    )

    await add_record(
        db,
        decision="REJECT",
        approved=False,
    )

    summary = (
        await build_execution_summary(
            db
        )
    )

    assert (
        summary.acceptance_rate
        == 0.5
    )

    assert (
        summary.execution_rate
        == 0.0
    )

    assert (
        summary.dry_run_rate
        == 1.0
    )


def test_summary_to_dict():

    summary = (
        ExecutionMonitoringSummary(
            total=10,
            accepted=3,
            rejected=2,
            watched=2,
            strong=3,
            gate_approved=6,
            gate_blocked=4,
            executed=0,
            dry_run=10,
        )
    )

    data = summary.to_dict()

    assert data["total"] == 10
    assert data["accepted"] == 3
    assert data["rejected"] == 2
    assert data["watched"] == 2
    assert data["strong"] == 3
    assert data["gate_approved"] == 6
    assert data["gate_blocked"] == 4
    assert data["executed"] == 0
    assert data["dry_run"] == 10
    assert data["acceptance_rate"] == 0.6
    assert data["execution_rate"] == 0.0
    assert data["dry_run_rate"] == 1.0