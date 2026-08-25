from backend.execution.audit import (
    ExecutionAuditRecord,
)

from backend.execution.audit_store import (
    ExecutionAuditStore,
)


def make_record(
    decision="ACCEPT",
    score=700,
    confidence=65,
    risk=40,
    approved=True,
):

    return (
        ExecutionAuditRecord.from_execution(
            decision=decision,
            score=score,
            confidence=confidence,
            risk=risk,
            gate_approved=approved,
            execution_enabled=True,
            executed=False,
            dry_run=True,
            message="Test audit record.",
        )
    )


def test_store_starts_empty():

    store = ExecutionAuditStore()

    assert store.count() == 0
    assert store.all() == []
    assert store.recent() == []


def test_add_returns_record():

    store = ExecutionAuditStore()

    record = make_record()

    result = store.add(record)

    assert result is record
    assert store.count() == 1


def test_added_record_can_be_retrieved():

    store = ExecutionAuditStore()

    record = make_record()

    store.add(record)

    records = store.all()

    assert len(records) == 1
    assert records[0] is record


def test_all_returns_copy():

    store = ExecutionAuditStore()

    store.add(
        make_record()
    )

    records = store.all()

    records.clear()

    assert store.count() == 1


def test_recent_returns_newest_first():

    store = ExecutionAuditStore()

    first = make_record(
        decision="WATCH",
        score=500,
    )

    second = make_record(
        decision="ACCEPT",
        score=700,
    )

    third = make_record(
        decision="STRONG",
        score=850,
    )

    store.add(first)
    store.add(second)
    store.add(third)

    recent = store.recent()

    assert recent == [
        third,
        second,
        first,
    ]


def test_recent_respects_limit():

    store = ExecutionAuditStore()

    first = make_record(
        decision="WATCH",
    )

    second = make_record(
        decision="ACCEPT",
    )

    third = make_record(
        decision="STRONG",
    )

    store.add(first)
    store.add(second)
    store.add(third)

    recent = store.recent(
        limit=2
    )

    assert recent == [
        third,
        second,
    ]


def test_recent_zero_returns_empty():

    store = ExecutionAuditStore()

    store.add(
        make_record()
    )

    assert (
        store.recent(0)
        == []
    )


def test_recent_negative_returns_empty():

    store = ExecutionAuditStore()

    store.add(
        make_record()
    )

    assert (
        store.recent(-1)
        == []
    )


def test_clear_removes_records():

    store = ExecutionAuditStore()

    store.add(
        make_record()
    )

    store.add(
        make_record(
            decision="STRONG"
        )
    )

    assert store.count() == 2

    store.clear()

    assert store.count() == 0
    assert store.all() == []


def test_constructor_can_accept_records():

    first = make_record(
        decision="WATCH"
    )

    second = make_record(
        decision="ACCEPT"
    )

    store = ExecutionAuditStore(
        records=[
            first,
            second,
        ]
    )

    assert store.count() == 2

    assert store.all() == [
        first,
        second,
    ]


def test_blocked_records_are_stored():

    store = ExecutionAuditStore()

    record = make_record(
        decision="REJECT",
        score=300,
        confidence=20,
        risk=90,
        approved=False,
    )

    store.add(record)

    stored = store.recent(1)[0]

    assert (
        stored.decision
        == "REJECT"
    )

    assert (
        stored.gate_approved
        is False
    )

    assert (
        stored.executed
        is False
    )

    assert (
        stored.dry_run
        is True
    )


def test_store_never_changes_execution_state():

    store = ExecutionAuditStore()

    record = make_record(
        decision="STRONG",
        score=850,
        confidence=80,
        risk=20,
    )

    store.add(record)

    stored = store.recent(1)[0]

    assert (
        stored.executed
        is False
    )

    assert (
        stored.dry_run
        is True
    )