from backend.intelligence.calibration_apply import (
    AdjustedSignal,
)

from backend.intelligence.decision import (
    IntelligenceDecisionEngine,
)


def make_signal(
    score,
    confidence,
    risk,
):
    return AdjustedSignal(
        original_score=score,
        adjusted_score=score,
        original_confidence=confidence,
        adjusted_confidence=confidence,
        original_risk=risk,
        adjusted_risk=risk,
    )


def test_strong_decision():

    signal = make_signal(
        score=850,
        confidence=80,
        risk=20,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "STRONG"
    )

    assert (
        result.score
        == 850.0
    )

    assert (
        result.confidence
        == 80.0
    )

    assert (
        result.risk
        == 20.0
    )


def test_accept_decision():

    signal = make_signal(
        score=700,
        confidence=65,
        risk=40,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "ACCEPT"
    )


def test_watch_decision():

    signal = make_signal(
        score=550,
        confidence=50,
        risk=60,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "WATCH"
    )


def test_reject_low_score():

    signal = make_signal(
        score=400,
        confidence=80,
        risk=20,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "REJECT"
    )


def test_reject_low_confidence():

    signal = make_signal(
        score=900,
        confidence=30,
        risk=20,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "REJECT"
    )


def test_high_risk_overrides_high_score():

    signal = make_signal(
        score=950,
        confidence=95,
        risk=80,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "REJECT"
    )


def test_boundary_strong():

    signal = make_signal(
        score=800,
        confidence=75,
        risk=30,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "STRONG"
    )


def test_boundary_accept():

    signal = make_signal(
        score=650,
        confidence=60,
        risk=50,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "ACCEPT"
    )


def test_boundary_watch():

    signal = make_signal(
        score=500,
        confidence=45,
        risk=70,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "WATCH"
    )


def test_risk_has_priority():

    signal = make_signal(
        score=800,
        confidence=80,
        risk=71,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    assert (
        result.decision
        == "REJECT"
    )


def test_to_dict():

    signal = make_signal(
        score=850,
        confidence=80,
        risk=20,
    )

    result = (
        IntelligenceDecisionEngine.evaluate(
            signal
        )
    )

    data = result.to_dict()

    assert (
        data["decision"]
        == "STRONG"
    )

    assert (
        data["score"]
        == 850.0
    )

    assert (
        data["confidence"]
        == 80.0
    )

    assert (
        data["risk"]
        == 20.0
    )

    assert (
        "reason"
        in data
    )


def test_original_signal_is_not_modified():

    signal = make_signal(
        score=850,
        confidence=80,
        risk=20,
    )

    original_score = (
        signal.original_score
    )

    original_confidence = (
        signal.original_confidence
    )

    original_risk = (
        signal.original_risk
    )

    IntelligenceDecisionEngine.evaluate(
        signal
    )

    assert (
        signal.original_score
        == original_score
    )

    assert (
        signal.original_confidence
        == original_confidence
    )

    assert (
        signal.original_risk
        == original_risk
    )