import pytest

from backend.feedback.performance import (
    PerformanceEngine,
)

from backend.signals.persistence import (
    SignalHistoryRecord,
)


def make_record(
    action="BUY",
    confidence=70,
    outcome=None,
    pnl=None,
):

    return SignalHistoryRecord(
        token_address="TEST123",
        symbol="TEST",
        action=action,
        score=750,
        confidence=confidence,
        risk="LOW",
        reason="Test signal",
        price_at_signal=1.25,
        outcome=outcome,
        pnl=pnl,
    )


def test_empty_history():

    metrics = (
        PerformanceEngine.calculate(
            []
        )
    )

    assert (
        metrics.total_signals
        == 0
    )

    assert (
        metrics.resolved_signals
        == 0
    )

    assert (
        metrics.unresolved_signals
        == 0
    )

    assert (
        metrics.wins
        == 0
    )

    assert (
        metrics.losses
        == 0
    )

    assert (
        metrics.win_rate
        == 0.0
    )

    assert (
        metrics.total_pnl
        == 0.0
    )


def test_basic_performance():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        ),
        make_record(
            outcome="LOSS",
            pnl=-5.0,
        ),
        make_record(),
    ]

    metrics = (
        PerformanceEngine.calculate(
            records
        )
    )

    assert (
        metrics.total_signals
        == 3
    )

    assert (
        metrics.resolved_signals
        == 2
    )

    assert (
        metrics.unresolved_signals
        == 1
    )

    assert (
        metrics.wins
        == 1
    )

    assert (
        metrics.losses
        == 1
    )

    assert (
        metrics.win_rate
        == 50.0
    )

    assert (
        metrics.total_pnl
        == 5.0
    )

    assert (
        metrics.average_pnl
        == 2.5
    )


def test_action_counts():

    records = [
        make_record(
            action="BUY",
        ),
        make_record(
            action="BUY",
        ),
        make_record(
            action="STRONG_BUY",
        ),
        make_record(
            action="WATCH",
        ),
        make_record(
            action="AVOID",
        ),
        make_record(
            action="HOLD",
        ),
    ]

    metrics = (
        PerformanceEngine.calculate(
            records
        )
    )

    assert (
        metrics.buy_signals
        == 2
    )

    assert (
        metrics.strong_buy_signals
        == 1
    )

    assert (
        metrics.watch_signals
        == 1
    )

    assert (
        metrics.avoid_signals
        == 1
    )

    assert (
        metrics.hold_signals
        == 1
    )


def test_average_confidence():

    records = [
        make_record(
            confidence=40,
        ),
        make_record(
            confidence=60,
        ),
        make_record(
            confidence=80,
        ),
    ]

    metrics = (
        PerformanceEngine.calculate(
            records
        )
    )

    assert (
        metrics.average_confidence
        == 60.0
    )


def test_win_rate_ignores_unresolved():

    records = [
        make_record(
            outcome="WIN",
            pnl=10,
        ),
        make_record(
            outcome="WIN",
            pnl=5,
        ),
        make_record(),
        make_record(),
    ]

    metrics = (
        PerformanceEngine.calculate(
            records
        )
    )

    assert (
        metrics.win_rate
        == 100.0
    )

    assert (
        metrics.resolved_signals
        == 2
    )

    assert (
        metrics.unresolved_signals
        == 2
    )


def test_action_performance():

    records = [
        make_record(
            action="BUY",
            outcome="WIN",
            pnl=10,
        ),
        make_record(
            action="BUY",
            outcome="LOSS",
            pnl=-5,
        ),
        make_record(
            action="WATCH",
            outcome="WIN",
            pnl=3,
        ),
    ]

    results = (
        PerformanceEngine.calculate_by_action(
            records
        )
    )

    assert (
        "BUY"
        in results
    )

    assert (
        "WATCH"
        in results
    )

    assert (
        results["BUY"].total_signals
        == 2
    )

    assert (
        results["BUY"].wins
        == 1
    )

    assert (
        results["BUY"].losses
        == 1
    )

    assert (
        results["WATCH"].wins
        == 1
    )


def test_confidence_buckets():

    records = [
        make_record(
            confidence=25,
            outcome="LOSS",
            pnl=-2,
        ),
        make_record(
            confidence=60,
            outcome="WIN",
            pnl=5,
        ),
        make_record(
            confidence=90,
            outcome="WIN",
            pnl=10,
        ),
    ]

    results = (
        PerformanceEngine.calculate_by_confidence(
            records
        )
    )

    assert (
        results["LOW"].total_signals
        == 1
    )

    assert (
        results["MEDIUM"].total_signals
        == 1
    )

    assert (
        results["HIGH"].total_signals
        == 1
    )

    assert (
        results["LOW"].losses
        == 1
    )

    assert (
        results["MEDIUM"].wins
        == 1
    )

    assert (
        results["HIGH"].wins
        == 1
    )


def test_to_dict():

    records = [
        make_record(
            outcome="WIN",
            pnl=12.5,
        )
    ]

    metrics = (
        PerformanceEngine.calculate(
            records
        )
    )

    data = metrics.to_dict()

    assert (
        data["total_signals"]
        == 1
    )

    assert (
        data["resolved_signals"]
        == 1
    )

    assert (
        data["wins"]
        == 1
    )

    assert (
        data["total_pnl"]
        == 12.5
    )

    assert (
        "win_rate"
        in data
    )

    assert (
        "average_confidence"
        in data
    )