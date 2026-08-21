from backend.intelligence.pipeline import (
    IntelligencePipeline,
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

    result = IntelligencePipeline.evaluate(
        historical_records=[],
        score=700,
        confidence=60,
        risk=30,
    )

    assert (
        result.recommendation.status
        == "INSUFFICIENT_DATA"
    )

    assert (
        result.calibration.status
        == "NEUTRAL"
    )

    assert (
        result.adjusted_signal.adjusted_score
        == 700.0
    )

    assert (
        result.adjusted_signal.adjusted_confidence
        == 60.0
    )

    assert (
        result.adjusted_signal.adjusted_risk
        == 30.0
    )


def test_pipeline_with_limited_history():

    records = [
        make_record(
            outcome="WIN",
            pnl=5.0,
        )
        for _ in range(5)
    ]

    result = IntelligencePipeline.evaluate(
        historical_records=records,
        score=700,
        confidence=60,
        risk=30,
    )

    assert (
        result.recommendation.status
        == "LIMITED_DATA"
    )

    assert (
        result.calibration.status
        == "OBSERVE"
    )

    assert (
        result.adjusted_signal.adjusted_score
        == 700.0
    )

    assert (
        result.adjusted_signal.adjusted_confidence
        == 60.0
    )


def test_pipeline_with_positive_history():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    result = IntelligencePipeline.evaluate(
        historical_records=records,
        score=700,
        confidence=60,
        risk=30,
    )

    assert (
        result.recommendation.status
        == "POSITIVE"
    )

    assert (
        result.calibration.status
        == "POSITIVE"
    )

    assert (
        result.adjusted_signal.adjusted_score
        > 700.0
    )

    assert (
        result.adjusted_signal.adjusted_confidence
        > 60.0
    )

    assert (
        result.adjusted_signal.adjusted_risk
        < 30.0
    )


def test_pipeline_with_negative_history():

    records = [
        make_record(
            outcome="LOSS",
            pnl=-10.0,
        )
        for _ in range(10)
    ]

    result = IntelligencePipeline.evaluate(
        historical_records=records,
        score=700,
        confidence=60,
        risk=30,
    )

    assert (
        result.recommendation.status
        == "NEGATIVE"
    )

    assert (
        result.calibration.status
        == "NEGATIVE"
    )

    assert (
        result.adjusted_signal.adjusted_score
        < 700.0
    )

    assert (
        result.adjusted_signal.adjusted_confidence
        < 60.0
    )

    assert (
        result.adjusted_signal.adjusted_risk
        > 30.0
    )


def test_pipeline_preserves_original_signal():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    result = IntelligencePipeline.evaluate(
        historical_records=records,
        score=725,
        confidence=72,
        risk=25,
    )

    assert (
        result.adjusted_signal.original_score
        == 725.0
    )

    assert (
        result.adjusted_signal.original_confidence
        == 72.0
    )

    assert (
        result.adjusted_signal.original_risk
        == 25.0
    )


def test_pipeline_result_to_dict():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    result = IntelligencePipeline.evaluate(
        historical_records=records,
        score=700,
        confidence=60,
        risk=30,
    )

    data = result.to_dict()

    assert (
        "recommendation"
        in data
    )

    assert (
        "calibration"
        in data
    )

    assert (
        "adjusted_signal"
        in data
    )

    assert (
        "status"
        in data["recommendation"]
    )

    assert (
        "confidence_multiplier"
        in data["calibration"]
    )

    assert (
        "adjusted_score"
        in data["adjusted_signal"]
    )


def test_pipeline_does_not_modify_history():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    original_outcomes = [
        record.outcome
        for record in records
    ]

    original_pnl = [
        record.pnl
        for record in records
    ]

    IntelligencePipeline.evaluate(
        historical_records=records,
        score=700,
        confidence=60,
        risk=30,
    )

    assert [
        record.outcome
        for record in records
    ] == original_outcomes

    assert [
        record.pnl
        for record in records
    ] == original_pnl