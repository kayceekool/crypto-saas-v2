from datetime import datetime, timezone

from backend.execution.audit import (
    ExecutionAuditRecord,
)


def test_audit_record_preserves_execution_state():

    record = (
        ExecutionAuditRecord.from_execution(
            decision="ACCEPT",
            score=700,
            confidence=65,
            risk=40,
            gate_approved=True,
            execution_enabled=True,
            executed=False,
            dry_run=True,
            message=(
                "Dry-run execution approved."
            ),
        )
    )

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


def test_audit_timestamp_is_utc():

    record = (
        ExecutionAuditRecord.from_execution(
            decision="WATCH",
            score=500,
            confidence=40,
            risk=70,
            gate_approved=False,
            execution_enabled=False,
            executed=False,
            dry_run=True,
            message="Blocked.",
        )
    )

    assert isinstance(
        record.created_at,
        datetime,
    )

    assert (
        record.created_at.tzinfo
        is not None
    )

    assert (
        record.created_at.utcoffset()
        == timezone.utc.utcoffset(
            record.created_at
        )
    )


def test_audit_record_is_immutable():

    record = (
        ExecutionAuditRecord.from_execution(
            decision="ACCEPT",
            score=700,
            confidence=65,
            risk=40,
            gate_approved=True,
            execution_enabled=True,
            executed=False,
            dry_run=True,
            message="Dry run.",
        )
    )

    try:
        record.score = 999
        assert False
    except AttributeError:
        pass


def test_to_dict_contains_complete_audit_data():

    record = (
        ExecutionAuditRecord.from_execution(
            decision="STRONG",
            score=850,
            confidence=80,
            risk=20,
            gate_approved=True,
            execution_enabled=True,
            executed=False,
            dry_run=True,
            message="Simulation.",
        )
    )

    data = record.to_dict()

    assert data["decision"] == "STRONG"
    assert data["score"] == 850.0
    assert data["confidence"] == 80.0
    assert data["risk"] == 20.0

    assert (
        data["gate_approved"]
        is True
    )

    assert (
        data["execution_enabled"]
        is True
    )

    assert (
        data["executed"]
        is False
    )

    assert (
        data["dry_run"]
        is True
    )

    assert (
        "created_at"
        in data
    )

    assert (
        "message"
        in data
    )


def test_blocked_execution_is_auditable():

    record = (
        ExecutionAuditRecord.from_execution(
            decision="REJECT",
            score=300,
            confidence=20,
            risk=90,
            gate_approved=False,
            execution_enabled=True,
            executed=False,
            dry_run=True,
            message=(
                "Execution blocked."
            ),
        )
    )

    assert (
        record.gate_approved
        is False
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