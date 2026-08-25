import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.core.database import Base

from backend.execution.audit_store import (
    ExecutionAuditStore,
)

from backend.execution.persistent_executor import (
    PersistentAuditedDryRunExecutor,
)

from backend.intelligence.risk_gate import (
    RiskGateResult,
)

from backend.storage.execution_audit_db import (
    list_recent_execution_audits,
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


def make_gate(
    approved=True,
    decision="ACCEPT",
    score=700,
    confidence=65,
    risk=40,
):

    return RiskGateResult(
        approved=approved,
        decision=decision,
        score=score,
        confidence=confidence,
        risk=risk,
        reason="Test gate result.",
    )


@pytest.mark.asyncio
async def test_approved_execution_is_persisted(
    db,
):

    store = ExecutionAuditStore()

    executor = (
        PersistentAuditedDryRunExecutor(
            db=db,
            audit_store=store,
        )
    )

    result = await executor.execute(
        make_gate()
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=10,
        )
    )

    assert len(records) == 1

    record = records[0]

    assert (
        record.decision
        == "ACCEPT"
    )

    assert (
        record.gate_approved
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
async def test_blocked_execution_is_persisted(
    db,
):

    executor = (
        PersistentAuditedDryRunExecutor(
            db=db
        )
    )

    result = await executor.execute(
        make_gate(
            approved=False,
            decision="REJECT",
            score=300,
            confidence=20,
            risk=90,
        )
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=10,
        )
    )

    assert len(records) == 1

    record = records[0]

    assert (
        record.decision
        == "REJECT"
    )

    assert (
        record.gate_approved
        is False
    )

    assert (
        record.executed
        is False
    )


@pytest.mark.asyncio
async def test_multiple_executions_are_persisted(
    db,
):

    executor = (
        PersistentAuditedDryRunExecutor(
            db=db
        )
    )

    await executor.execute(
        make_gate(
            decision="WATCH",
            score=500,
            confidence=40,
            risk=70,
            approved=False,
        )
    )

    await executor.execute(
        make_gate(
            decision="ACCEPT",
            score=700,
            confidence=65,
            risk=40,
        )
    )

    await executor.execute(
        make_gate(
            decision="STRONG",
            score=850,
            confidence=80,
            risk=20,
        )
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


@pytest.mark.asyncio
async def test_persistent_record_matches_memory_audit(
    db,
):

    store = ExecutionAuditStore()

    executor = (
        PersistentAuditedDryRunExecutor(
            db=db,
            audit_store=store,
        )
    )

    result = await executor.execute(
        make_gate(
            decision="STRONG",
            score=850,
            confidence=80,
            risk=20,
        )
    )

    memory_record = (
        store.recent(1)[0]
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=1,
        )
    )

    database_record = records[0]

    assert (
        database_record.decision
        == memory_record.decision
    )

    assert (
        database_record.score
        == memory_record.score
    )

    assert (
        database_record.confidence
        == memory_record.confidence
    )

    assert (
        database_record.risk
        == memory_record.risk
    )

    assert (
        database_record.gate_approved
        == memory_record.gate_approved
    )

    assert (
        database_record.executed
        == memory_record.executed
    )

    assert (
        database_record.dry_run
        == memory_record.dry_run
    )

    assert (
        result.executed
        is False
    )


@pytest.mark.asyncio
async def test_strong_signal_remains_dry_run_after_persistence(
    db,
):

    executor = (
        PersistentAuditedDryRunExecutor(
            db=db
        )
    )

    result = await executor.execute(
        make_gate(
            decision="STRONG",
            score=950,
            confidence=95,
            risk=10,
        )
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=1,
        )
    )

    assert (
        records[0].executed
        is False
    )

    assert (
        records[0].dry_run
        is True
    )


@pytest.mark.asyncio
async def test_database_audit_has_message(
    db,
):

    executor = (
        PersistentAuditedDryRunExecutor(
            db=db
        )
    )

    await executor.execute(
        make_gate()
    )

    records = (
        await list_recent_execution_audits(
            db,
            limit=1,
        )
    )

    assert records[0].message
    assert (
        "Dry-run"
        in records[0].message
    )