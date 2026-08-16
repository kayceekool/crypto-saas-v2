from backend.feedback.performance import (
    PerformanceEngine,
)

from backend.feedback.recommendations import (
    FeedbackEngine,
)

from backend.intelligence.calibration import (
    CalibrationEngine,
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


def get_recommendation(
    records,
):

    metrics = (
        PerformanceEngine.calculate(
            records
        )
    )

    return FeedbackEngine.evaluate(
        metrics
    )


def test_insufficient_data_is_neutral():

    recommendation = (
        get_recommendation(
            [
                make_record(),
            ]
        )
    )

    profile = (
        CalibrationEngine.from_feedback(
            recommendation
        )
    )

    assert (
        profile.status
        == "NEUTRAL"
    )

    assert (
        profile.confidence_multiplier
        == 1.0
    )

    assert (
        profile.score_adjustment
        == 0.0
    )

    assert (
        profile.risk_adjustment
        == 0.0
    )


def test_limited_data_does_not_calibrate():

    records = [
        make_record(
            outcome="WIN",
            pnl=5.0,
        )
        for _ in range(5)
    ]

    recommendation = (
        get_recommendation(
            records
        )
    )

    profile = (
        CalibrationEngine.from_feedback(
            recommendation
        )
    )

    assert (
        recommendation.status
        == "LIMITED_DATA"
    )

    assert (
        profile.status
        == "OBSERVE"
    )

    assert (
        profile.confidence_multiplier
        == 1.0
    )

    assert (
        profile.score_adjustment
        == 0.0
    )


def test_positive_feedback_calibrates_upward():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    recommendation = (
        get_recommendation(
            records
        )
    )

    profile = (
        CalibrationEngine.from_feedback(
            recommendation
        )
    )

    assert (
        recommendation.status
        == "POSITIVE"
    )

    assert (
        profile.status
        == "POSITIVE"
    )

    assert (
        profile.confidence_multiplier
        > 1.0
    )

    assert (
        profile.score_adjustment
        > 0.0
    )

    assert (
        profile.risk_adjustment
        < 0.0
    )


def test_negative_feedback_calibrates_downward():

    records = [
        make_record(
            outcome="LOSS",
            pnl=-10.0,
        )
        for _ in range(10)
    ]

    recommendation = (
        get_recommendation(
            records
        )
    )

    profile = (
        CalibrationEngine.from_feedback(
            recommendation
        )
    )

    assert (
        recommendation.status
        == "NEGATIVE"
    )

    assert (
        profile.status
        == "NEGATIVE"
    )

    assert (
        profile.confidence_multiplier
        < 1.0
    )

    assert (
        profile.score_adjustment
        < 0.0
    )

    assert (
        profile.risk_adjustment
        > 0.0
    )


def test_calibration_is_bounded():

    records = [
        make_record(
            outcome="WIN",
            pnl=100.0,
        )
        for _ in range(100)
    ]

    recommendation = (
        get_recommendation(
            records
        )
    )

    profile = (
        CalibrationEngine.from_feedback(
            recommendation
        )
    )

    assert (
        CalibrationEngine.MIN_MULTIPLIER
        <= profile.confidence_multiplier
        <= CalibrationEngine.MAX_MULTIPLIER
    )

    assert (
        CalibrationEngine.MIN_SCORE_ADJUSTMENT
        <= profile.score_adjustment
        <= CalibrationEngine.MAX_SCORE_ADJUSTMENT
    )

    assert (
        CalibrationEngine.MIN_RISK_ADJUSTMENT
        <= profile.risk_adjustment
        <= CalibrationEngine.MAX_RISK_ADJUSTMENT
    )


def test_to_dict():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    recommendation = (
        get_recommendation(
            records
        )
    )

    profile = (
        CalibrationEngine.from_feedback(
            recommendation
        )
    )

    data = profile.to_dict()

    assert (
        "confidence_multiplier"
        in data
    )

    assert (
        "score_adjustment"
        in data
    )

    assert (
        "risk_adjustment"
        in data
    )

    assert (
        "status"
        in data
    )

    assert (
        "reason"
        in data
    )