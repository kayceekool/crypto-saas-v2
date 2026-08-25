from backend.intelligence.decision_pipeline import (
    IntelligenceDecisionPipeline,
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


def test_pipeline_with_no_history():

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=[],
            score=700,
            confidence=60,
            risk=30,
        )
    )

    assert (
        result.decision.decision
        == "ACCEPT"
    )

    assert (
        result.intelligence.recommendation.status
        == "INSUFFICIENT_DATA"
    )

    assert (
        result.intelligence.adjusted_signal.adjusted_score
        == 700.0
    )


def test_positive_history_can_produce_strong():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=records,
            score=800,
            confidence=75,
            risk=30,
        )
    )

    assert (
        result.intelligence.recommendation.status
        == "POSITIVE"
    )

    assert (
        result.intelligence.calibration.status
        == "POSITIVE"
    )

    assert (
        result.decision.decision
        == "STRONG"
    )


def test_negative_history_reduces_signal():

    records = [
        make_record(
            outcome="LOSS",
            pnl=-10.0,
        )
        for _ in range(10)
    ]

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=records,
            score=700,
            confidence=60,
            risk=30,
        )
    )

    assert (
        result.intelligence.recommendation.status
        == "NEGATIVE"
    )

    assert (
        result.intelligence.adjusted_signal.adjusted_score
        < 700.0
    )

    assert (
        result.intelligence.adjusted_signal.adjusted_confidence
        < 60.0
    )


def test_high_risk_is_rejected():

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=[],
            score=950,
            confidence=95,
            risk=80,
        )
    )

    assert (
        result.decision.decision
        == "REJECT"
    )


def test_watch_classification():

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=[],
            score=550,
            confidence=50,
            risk=60,
        )
    )

    assert (
        result.decision.decision
        == "WATCH"
    )


def test_accept_classification():

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=[],
            score=700,
            confidence=65,
            risk=40,
        )
    )

    assert (
        result.decision.decision
        == "ACCEPT"
    )


def test_result_to_dict():

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=[],
            score=700,
            confidence=65,
            risk=40,
        )
    )

    data = result.to_dict()

    assert (
        "intelligence"
        in data
    )

    assert (
        "decision"
        in data
    )

    assert (
        "recommendation"
        in data["intelligence"]
    )

    assert (
        "calibration"
        in data["intelligence"]
    )

    assert (
        "adjusted_signal"
        in data["intelligence"]
    )

    assert (
        data["decision"]["decision"]
        == "ACCEPT"
    )


def test_original_signal_is_preserved():

    result = (
        IntelligenceDecisionPipeline.evaluate(
            historical_records=[],
            score=725,
            confidence=72,
            risk=25,
        )
    )

    adjusted = (
        result.intelligence.adjusted_signal
    )

    assert (
        adjusted.original_score
        == 725.0
    )

    assert (
        adjusted.original_confidence
        == 72.0
    )

    assert (
        adjusted.original_risk
        == 25.0
    )