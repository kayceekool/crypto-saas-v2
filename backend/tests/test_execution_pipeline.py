from backend.execution.pipeline import (
    ExecutionPipeline,
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


def test_complete_pipeline_defaults_to_dry_run():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=700,
        confidence=65,
        risk=40,
    )

    assert (
        result.execution.executed
        is False
    )

    assert (
        result.execution.dry_run
        is True
    )

    assert (
        result.gate.approved
        is False
    )

    assert (
        result.intelligence.decision.decision
        == "ACCEPT"
    )


def test_complete_pipeline_can_pass_risk_gate():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=700,
        confidence=65,
        risk=40,
        execution_enabled=True,
    )

    assert (
        result.gate.approved
        is True
    )

    assert (
        result.execution.executed
        is False
    )

    assert (
        result.execution.dry_run
        is True
    )

    assert (
        result.execution.decision
        == "ACCEPT"
    )


def test_strong_signal_reaches_dry_run():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=850,
        confidence=80,
        risk=20,
        execution_enabled=True,
    )

    assert (
        result.intelligence.decision.decision
        == "STRONG"
    )

    assert (
        result.gate.approved
        is True
    )

    assert (
        result.execution.executed
        is False
    )

    assert (
        result.execution.dry_run
        is True
    )


def test_watch_signal_is_blocked():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=550,
        confidence=50,
        risk=60,
        execution_enabled=True,
    )

    assert (
        result.intelligence.decision.decision
        == "WATCH"
    )

    assert (
        result.gate.approved
        is False
    )

    assert (
        result.execution.executed
        is False
    )


def test_high_risk_signal_is_blocked():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=950,
        confidence=95,
        risk=80,
        execution_enabled=True,
    )

    assert (
        result.intelligence.decision.decision
        == "REJECT"
    )

    assert (
        result.gate.approved
        is False
    )

    assert (
        result.execution.executed
        is False
    )


def test_positive_history_flows_through_pipeline():

    records = [
        make_record(
            outcome="WIN",
            pnl=10.0,
        )
        for _ in range(10)
    ]

    result = ExecutionPipeline.evaluate(
        historical_records=records,
        score=800,
        confidence=75,
        risk=30,
        execution_enabled=True,
    )

    intelligence = result.intelligence.intelligence

    assert (
        intelligence
        .recommendation
        .status
        == "POSITIVE"
    )

    assert (
        intelligence
        .calibration
        .status
        == "POSITIVE"
    )

    assert (
        result.intelligence
        .decision
        .decision
        == "STRONG"
    )

    assert (
        result.gate.approved
        is True
    )

    assert (
        result.execution.executed
        is False
    )

    assert (
        result.execution.dry_run
        is True
    )


def test_negative_history_flows_through_pipeline():

    records = [
        make_record(
            outcome="LOSS",
            pnl=-10.0,
        )
        for _ in range(10)
    ]

    result = ExecutionPipeline.evaluate(
        historical_records=records,
        score=700,
        confidence=60,
        risk=30,
        execution_enabled=True,
    )

    intelligence = result.intelligence.intelligence

    assert (
        intelligence
        .recommendation
        .status
        == "NEGATIVE"
    )

    assert (
        intelligence
        .adjusted_signal
        .adjusted_score
        < 700.0
    )

    assert (
        intelligence
        .adjusted_signal
        .adjusted_confidence
        < 60.0
    )

    assert (
        result.execution.executed
        is False
    )


def test_execution_disabled_cannot_be_overridden():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=900,
        confidence=90,
        risk=20,
        execution_enabled=False,
    )

    assert (
        result.gate.approved
        is False
    )

    assert (
        result.execution.executed
        is False
    )

    assert (
        result.execution.dry_run
        is True
    )


def test_result_to_dict():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=700,
        confidence=65,
        risk=40,
        execution_enabled=True,
    )

    data = result.to_dict()

    assert (
        "intelligence"
        in data
    )

    assert (
        "gate"
        in data
    )

    assert (
        "execution"
        in data
    )

    assert (
        "decision"
        in data["intelligence"]
    )

    assert (
        "approved"
        in data["gate"]
    )

    assert (
        "executed"
        in data["execution"]
    )

    assert (
        data["execution"]["dry_run"]
        is True
    )


def test_no_real_execution_is_possible():

    result = ExecutionPipeline.evaluate(
        historical_records=[],
        score=950,
        confidence=95,
        risk=10,
        execution_enabled=True,
    )

    assert (
        result.gate.approved
        is True
    )

    assert (
        result.execution.executed
        is False
    )

    assert (
        result.execution.dry_run
        is True
    )