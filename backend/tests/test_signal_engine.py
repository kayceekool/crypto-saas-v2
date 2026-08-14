from datetime import datetime

from backend.intelligence.persistence import (
    IntelligenceRecord,
)

from backend.signals.signal_engine import (
    SignalEngine,
)


def make_record(
    score=850,
    confidence=80,
    risk="LOW",
    signal="STRONG",
):

    return IntelligenceRecord(
        token_address="TEST123",
        symbol="TEST",
        score=score,
        confidence=confidence,
        pattern="BREAKOUT",
        risk=risk,
        signal=signal,
        price=1.25,
        liquidity=50000,
        volume=100000,
        metadata={},
    )


def test_strong_buy():

    record = make_record(
        score=850,
        confidence=80,
        risk="LOW",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert (
        decision.action
        == "STRONG_BUY"
    )

    assert (
        decision.score
        == 850
    )

    assert (
        decision.confidence
        == 80
    )


def test_buy():

    record = make_record(
        score=700,
        confidence=60,
        risk="LOW",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert decision.action == "BUY"


def test_watch():

    record = make_record(
        score=500,
        confidence=40,
        risk="LOW",
        signal="WATCH",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert decision.action == "WATCH"


def test_high_risk_is_avoid():

    record = make_record(
        score=950,
        confidence=95,
        risk="HIGH",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert decision.action == "AVOID"


def test_hold():

    record = make_record(
        score=200,
        confidence=20,
        risk="LOW",
        signal="NONE",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert decision.action == "HOLD"


def test_signal_fallback_to_watch():

    record = make_record(
        score=300,
        confidence=60,
        risk="LOW",
        signal="BUY",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert decision.action == "WATCH"


def test_unknown_risk_is_not_automatically_buy():

    record = make_record(
        score=700,
        confidence=60,
        risk="UNKNOWN",
    )

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    assert decision.action == "BUY"


def test_created_at_is_generated():

    before = datetime.utcnow()

    record = make_record()

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    after = datetime.utcnow()

    assert (
        before
        <= decision.created_at
        <= after
    )


def test_to_dict():

    record = make_record()

    decision = (
        SignalEngine.evaluate(
            record
        )
    )

    data = decision.to_dict()

    assert (
        data["token_address"]
        == "TEST123"
    )

    assert (
        data["symbol"]
        == "TEST"
    )

    assert (
        data["action"]
        == "STRONG_BUY"
    )

    assert (
        "reason"
        in data
    )

    assert (
        "created_at"
        in data
    )


def test_evaluate_many():

    records = [
        make_record(
            score=900,
            confidence=90,
        ),
        make_record(
            score=700,
            confidence=60,
        ),
        make_record(
            score=200,
            confidence=20,
            signal="NONE",
        ),
    ]

    decisions = (
        SignalEngine.evaluate_many(
            records
        )
    )

    assert len(decisions) == 3

    assert (
        decisions[0].action
        == "STRONG_BUY"
    )

    assert (
        decisions[1].action
        == "BUY"
    )

    assert (
        decisions[2].action
        == "HOLD"
    )