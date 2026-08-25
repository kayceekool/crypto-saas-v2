from backend.execution.audit_store import (
    ExecutionAuditStore,
)

from backend.execution.audited_executor import (
    AuditedDryRunExecutor,
)

from backend.intelligence.risk_gate import (
    RiskGateResult,
)


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


def test_approved_execution_is_audited():

    store = ExecutionAuditStore()

    executor = (
        AuditedDryRunExecutor(
            audit_store=store
        )
    )

    result = executor.execute(
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

    assert (
        store.count()
        == 1
    )


def test_audit_contains_execution_result():

    store = ExecutionAuditStore()

    executor = (
        AuditedDryRunExecutor(
            audit_store=store
        )
    )

    executor.execute(
        make_gate(
            decision="STRONG",
            score=850,
            confidence=80,
            risk=20,
        )
    )

    record = store.recent(1)[0]

    assert (
        record.decision
        == "STRONG"
    )

    assert (
        record.score
        == 850.0
    )

    assert (
        record.confidence
        == 80.0
    )

    assert (
        record.risk
        == 20.0
    )

    assert (
        record.executed
        is False
    )

    assert (
        record.dry_run
        is True
    )


def test_blocked_execution_is_audited():

    store = ExecutionAuditStore()

    executor = (
        AuditedDryRunExecutor(
            audit_store=store
        )
    )

    result = executor.execute(
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

    assert (
        store.count()
        == 1
    )

    record = store.recent(1)[0]

    assert (
        record.gate_approved
        is False
    )

    assert (
        record.decision
        == "REJECT"
    )


def test_multiple_executions_create_multiple_audits():

    store = ExecutionAuditStore()

    executor = (
        AuditedDryRunExecutor(
            audit_store=store
        )
    )

    executor.execute(
        make_gate(
            decision="WATCH"
        )
    )

    executor.execute(
        make_gate(
            decision="ACCEPT"
        )
    )

    executor.execute(
        make_gate(
            decision="STRONG"
        )
    )

    assert (
        store.count()
        == 3
    )

    records = store.recent(3)

    assert [
        record.decision
        for record in records
    ] == [
        "STRONG",
        "ACCEPT",
        "WATCH",
    ]


def test_executor_creates_default_store():

    executor = (
        AuditedDryRunExecutor()
    )

    result = executor.execute(
        make_gate()
    )

    assert (
        result.executed
        is False
    )

    assert (
        executor.audit_store.count()
        == 1
    )


def test_audit_state_matches_execution_state():

    store = ExecutionAuditStore()

    executor = (
        AuditedDryRunExecutor(
            audit_store=store
        )
    )

    result = executor.execute(
        make_gate()
    )

    record = store.recent(1)[0]

    assert (
        record.executed
        == result.executed
    )

    assert (
        record.dry_run
        == result.dry_run
    )


def test_no_real_execution_occurs():

    store = ExecutionAuditStore()

    executor = (
        AuditedDryRunExecutor(
            audit_store=store
        )
    )

    result = executor.execute(
        make_gate(
            approved=True,
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

    record = store.recent(1)[0]

    assert (
        record.executed
        is False
    )

    assert (
        record.dry_run
        is True
    )