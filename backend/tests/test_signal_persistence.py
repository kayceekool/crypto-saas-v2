from datetime import datetime

from backend.signals.models import (
    SignalDecision,
)

from backend.storage.signal_repository import (
    SignalRepository,
)


def make_decision():

    return SignalDecision(
        token_address="TEST123",
        symbol="TEST",
        action="BUY",
        score=750,
        confidence=70,
        risk="LOW",
        reason=(
            "Score and confidence "
            "meet the buy threshold."
        ),
        created_at=datetime.utcnow(),
    )


def test_decision_to_history():

    decision = make_decision()

    record = (
        SignalRepository.from_decision(
            decision,
            price=1.25,
        )
    )

    assert (
        record.token_address
        == "TEST123"
    )

    assert (
        record.symbol
        == "TEST"
    )

    assert (
        record.action
        == "BUY"
    )

    assert (
        record.score
        == 750
    )

    assert (
        record.confidence
        == 70
    )

    assert (
        record.price_at_signal
        == 1.25
    )


def test_history_is_unresolved_initially():

    record = (
        SignalRepository.from_decision(
            make_decision()
        )
    )

    assert record.outcome is None

    assert record.pnl is None

    assert record.resolved_at is None


def test_resolve_signal():

    record = (
        SignalRepository.from_decision(
            make_decision()
        )
    )

    SignalRepository.resolve(
        record,
        outcome="WIN",
        pnl=12.5,
    )

    assert (
        record.outcome
        == "WIN"
    )

    assert (
        record.pnl
        == 12.5
    )

    assert (
        record.resolved_at
        is not None
    )


def test_negative_outcome():

    record = (
        SignalRepository.from_decision(
            make_decision()
        )
    )

    SignalRepository.resolve(
        record,
        outcome="LOSS",
        pnl=-7.25,
    )

    assert (
        record.outcome
        == "LOSS"
    )

    assert (
        record.pnl
        == -7.25
    )


def test_multiple_decisions():

    decisions = [
        make_decision(),
        make_decision(),
        make_decision(),
    ]

    records = (
        SignalRepository.from_decisions(
            decisions
        )
    )

    assert len(records) == 3


def test_serialization():

    record = (
        SignalRepository.from_decision(
            make_decision(),
            price=2.50,
        )
    )

    data = record.to_dict()

    assert (
        data["token_address"]
        == "TEST123"
    )

    assert (
        data["action"]
        == "BUY"
    )

    assert (
        data["price_at_signal"]
        == 2.50
    )

    assert (
        data["outcome"]
        is None
    )


def test_resolved_serialization():

    record = (
        SignalRepository.from_decision(
            make_decision(),
            price=2.50,
        )
    )

    SignalRepository.resolve(
        record,
        outcome="WIN",
        pnl=25.0,
    )

    data = record.to_dict()

    assert (
        data["outcome"]
        == "WIN"
    )

    assert (
        data["pnl"]
        == 25.0
    )

    assert (
        data["resolved_at"]
        is not None
    )