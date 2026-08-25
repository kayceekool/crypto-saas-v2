from backend.intelligence.decision import (
    IntelligenceDecision,
)

from backend.intelligence.risk_gate import (
    RiskGate,
)


def make_decision(
    decision="ACCEPT",
    score=700,
    confidence=65,
    risk=40,
):
    return IntelligenceDecision(
        decision=decision,
        score=score,
        confidence=confidence,
        risk=risk,
        reason="Test decision",
    )


def test_execution_disabled_by_default():

    decision = make_decision()

    result = RiskGate.evaluate(
        decision
    )

    assert (
        result.approved
        is False
    )

    assert (
        "not explicitly enabled"
        in result.reason
    )


def test_accept_can_pass_when_enabled():

    decision = make_decision(
        decision="ACCEPT",
        score=700,
        confidence=65,
        risk=40,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is True
    )

    assert (
        result.decision
        == "ACCEPT"
    )


def test_strong_can_pass_when_enabled():

    decision = make_decision(
        decision="STRONG",
        score=850,
        confidence=80,
        risk=20,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is True
    )


def test_watch_is_blocked():

    decision = make_decision(
        decision="WATCH",
        score=550,
        confidence=50,
        risk=40,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is False
    )


def test_reject_is_blocked():

    decision = make_decision(
        decision="REJECT",
        score=900,
        confidence=90,
        risk=20,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is False
    )


def test_low_score_is_blocked():

    decision = make_decision(
        decision="ACCEPT",
        score=649,
        confidence=90,
        risk=20,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is False
    )


def test_low_confidence_is_blocked():

    decision = make_decision(
        decision="ACCEPT",
        score=700,
        confidence=59,
        risk=20,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is False
    )


def test_high_risk_is_blocked():

    decision = make_decision(
        decision="ACCEPT",
        score=700,
        confidence=80,
        risk=51,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is False
    )


def test_exact_thresholds_are_allowed():

    decision = make_decision(
        decision="ACCEPT",
        score=650,
        confidence=60,
        risk=50,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    assert (
        result.approved
        is True
    )


def test_result_preserves_values():

    decision = make_decision(
        decision="STRONG",
        score=850,
        confidence=80,
        risk=20,
    )

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
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


def test_to_dict():

    decision = make_decision()

    result = RiskGate.evaluate(
        decision,
        execution_enabled=True,
    )

    data = result.to_dict()

    assert (
        data["approved"]
        is True
    )

    assert (
        data["decision"]
        == "ACCEPT"
    )

    assert (
        data["score"]
        == 700.0
    )

    assert (
        data["confidence"]
        == 65.0
    )

    assert (
        data["risk"]
        == 40.0
    )

    assert (
        "reason"
        in data
    )