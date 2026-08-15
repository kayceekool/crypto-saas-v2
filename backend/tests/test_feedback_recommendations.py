from backend.feedback.performance import (
    PerformanceEngine,
)

from backend.feedback.recommendations import (
    FeedbackEngine,
)


def make_record(
    outcome=None,
    pnl=None,
):
    from backend.signals.persistence import (
        SignalHistoryRecord,
    )

    return SignalHistoryRecord(
        token_address="TEST123",
        symbol="TEST",
        action="BUY",
        score=750,
        confidence=80,
        risk="LOW",
        reason="Test signal",
        price_at_signal=1.25,
        outcome=outcome,
        pnl=pnl,
    )


def test_no_resolved_signals():

    metrics = PerformanceEngine.calculate(
        [
            make_record(),
            make_record(),
        ]
    )

    recommendation = (
        FeedbackEngine.evaluate(
            metrics
        )
    )

    assert (
        recommendation.status
        == "INSUFFICIENT_DATA"
    )

    assert (
        recommendation.suggested_action
        == "COLLECT_MORE_OUTCOMES"
    )

    assert (
        recommendation.confidence
        == 0.0
    )


def test_limited_data():

    records = [
        make_record(
            outcome="WIN",
            pnl=5.0,
        )
        for _ in range(5)
    ]

    metrics = PerformanceEngine.calculate(
        records
    )

    recommendation = (
        FeedbackEngine.evaluate(
            metrics
        )
    )

    assert (
        recommendation.status
        == "LIMITED_DATA"
    )

    assert (
        recommendation.suggested_action
        == "CONTINUE_OBSERVATION"
    )

    assert (
        recommendation.resolved_signals
        == 5
    )


def test_positive_performance():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    metrics = PerformanceEngine.calculate(
        records
    )

    recommendation = (
        FeedbackEngine.evaluate(
            metrics
        )
    )

    assert (
        recommendation.status
        == "POSITIVE"
    )

    assert (
        recommendation.suggested_action
        == "MAINTAIN_CONFIGURATION"
    )

    assert (
        recommendation.win_rate
        == 100.0
    )

    assert (
        recommendation.average_pnl
        == 10.0
    )


def test_negative_performance():

    records = [
        make_record(
            outcome="LOSS",
            pnl=-5.0,
        )
        for _ in range(10)
    ]

    metrics = PerformanceEngine.calculate(
        records
    )

    recommendation = (
        FeedbackEngine.evaluate(
            metrics
        )
    )

    assert (
        recommendation.status
        == "NEGATIVE"
    )

    assert (
        recommendation.suggested_action
        == "REVIEW_CONFIGURATION"
    )

    assert (
        recommendation.win_rate
        == 0.0
    )

    assert (
        recommendation.total_pnl
        == -50.0
    )


def test_neutral_performance():

    records = [
        make_record(
            outcome="WIN",
            pnl=5.0,
        )
        for _ in range(5)
    ]

    records.extend(
        [
            make_record(
                outcome="LOSS",
                pnl=-5.0,
            )
            for _ in range(5)
        ]
    )

    metrics = PerformanceEngine.calculate(
        records
    )

    recommendation = (
        FeedbackEngine.evaluate(
            metrics
        )
    )

    assert (
        recommendation.status
        == "NEUTRAL"
    )

    assert (
        recommendation.suggested_action
        == "CONTINUE_OBSERVATION"
    )

    assert (
        recommendation.win_rate
        == 50.0
    )


def test_to_dict():

    records = [
        make_record(
            outcome="WIN",
            pnl=8.5,
        )
        for _ in range(10)
    ]

    metrics = PerformanceEngine.calculate(
        records
    )

    recommendation = (
        FeedbackEngine.evaluate(
            metrics
        )
    )

    data = recommendation.to_dict()

    assert (
        data["status"]
        == "POSITIVE"
    )

    assert (
        data["suggested_action"]
        == "MAINTAIN_CONFIGURATION"
    )

    assert (
        data["win_rate"]
        == 100.0
    )

    assert (
        data["total_pnl"]
        == 85.0
    )

    assert (
        "confidence"
        in data
    )

    assert (
        "message"
        in data
    )