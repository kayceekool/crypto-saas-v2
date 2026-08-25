from backend.execution.dry_run import (
    DryRunExecutor,
)

from backend.intelligence.risk_gate import (
    RiskGateResult,
)


def make_gate_result(
    approved=True,
    decision="ACCEPT",
    score=700,
    confidence=65,
    risk=40,
):
    return RiskGateResult(
        approved=approved,
        decision=decision,
        score=score,
        confidence=confidence,
        risk=risk,
        reason="Test risk-gate result",
    )


def test_approved_signal_is_simulated():

    gate_result = make_gate_result(
        approved=True,
    )

    result = DryRunExecutor.execute(
        gate_result
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    assert (
        result.decision
        == "ACCEPT"
    )

    assert (
        result.score
        == 700.0
    )

    assert (
        result.confidence
        == 65.0
    )

    assert (
        result.risk
        == 40.0
    )

    assert (
        "No transaction"
        in result.message
    )


def test_blocked_signal_is_not_executed():

    gate_result = make_gate_result(
        approved=False,
        decision="REJECT",
    )

    result = DryRunExecutor.execute(
        gate_result
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    assert (
        result.decision
        == "REJECT"
    )

    assert (
        "blocked"
        in result.message.lower()
    )


def test_watch_signal_is_not_executed():

    gate_result = make_gate_result(
        approved=False,
        decision="WATCH",
        score=550,
        confidence=50,
        risk=60,
    )

    result = DryRunExecutor.execute(
        gate_result
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    assert (
        result.decision
        == "WATCH"
    )


def test_strong_signal_remains_dry_run():

    gate_result = make_gate_result(
        approved=True,
        decision="STRONG",
        score=850,
        confidence=80,
        risk=20,
    )

    result = DryRunExecutor.execute(
        gate_result
    )

    assert (
        result.executed
        is False
    )

    assert (
        result.dry_run
        is True
    )

    assert (
        result.decision
        == "STRONG"
    )


def test_result_to_dict():

    gate_result = make_gate_result()

    result = DryRunExecutor.execute(
        gate_result
    )

    data = result.to_dict()

    assert (
        data["executed"]
        is False
    )

    assert (
        data["dry_run"]
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
        "message"
        in data
    )


def test_executor_never_reports_real_execution():

    for approved in (
        True,
        False,
    ):

        gate_result = make_gate_result(
            approved=approved,
        )

        result = DryRunExecutor.execute(
            gate_result
        )

        assert (
            result.executed
            is False
        )

        assert (
            result.dry_run
            is True
        )