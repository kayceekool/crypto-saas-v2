from backend.intelligence.calibration import (
    CalibrationProfile,
)

from backend.intelligence.calibration_apply import (
    CalibrationApplier,
)


def positive_profile():

    return CalibrationProfile(
        confidence_multiplier=1.10,
        score_adjustment=5.0,
        risk_adjustment=-2.0,
        status="POSITIVE",
        reason="Positive test profile",
    )


def negative_profile():

    return CalibrationProfile(
        confidence_multiplier=0.90,
        score_adjustment=-5.0,
        risk_adjustment=2.0,
        status="NEGATIVE",
        reason="Negative test profile",
    )


def neutral_profile():

    return CalibrationProfile(
        confidence_multiplier=1.0,
        score_adjustment=0.0,
        risk_adjustment=0.0,
        status="NEUTRAL",
        reason="Neutral test profile",
    )


def test_positive_calibration():

    result = CalibrationApplier.apply(
        score=700,
        confidence=60,
        risk=30,
        profile=positive_profile(),
    )

    assert (
        result.original_score
        == 700.0
    )

    assert (
        result.adjusted_score
        == 705.0
    )

    assert (
        result.original_confidence
        == 60.0
    )

    assert (
        result.adjusted_confidence
        == 66.0
    )

    assert (
        result.original_risk
        == 30.0
    )

    assert (
        result.adjusted_risk
        == 28.0
    )


def test_negative_calibration():

    result = CalibrationApplier.apply(
        score=700,
        confidence=60,
        risk=30,
        profile=negative_profile(),
    )

    assert (
        result.adjusted_score
        == 695.0
    )

    assert (
        result.adjusted_confidence
        == 54.0
    )

    assert (
        result.adjusted_risk
        == 32.0
    )


def test_neutral_calibration():

    result = CalibrationApplier.apply(
        score=700,
        confidence=60,
        risk=30,
        profile=neutral_profile(),
    )

    assert (
        result.adjusted_score
        == 700.0
    )

    assert (
        result.adjusted_confidence
        == 60.0
    )

    assert (
        result.adjusted_risk
        == 30.0
    )


def test_score_lower_bound():

    profile = CalibrationProfile(
        confidence_multiplier=1.0,
        score_adjustment=-5.0,
        risk_adjustment=0.0,
        status="NEGATIVE",
        reason="Lower bound test",
    )

    result = CalibrationApplier.apply(
        score=1,
        confidence=50,
        risk=20,
        profile=profile,
    )

    assert (
        result.adjusted_score
        == 0.0
    )


def test_score_upper_bound():

    profile = CalibrationProfile(
        confidence_multiplier=1.0,
        score_adjustment=5.0,
        risk_adjustment=0.0,
        status="POSITIVE",
        reason="Upper bound test",
    )

    result = CalibrationApplier.apply(
        score=1000,
        confidence=50,
        risk=20,
        profile=profile,
    )

    assert (
        result.adjusted_score
        == 1000.0
    )


def test_confidence_upper_bound():

    profile = CalibrationProfile(
        confidence_multiplier=1.10,
        score_adjustment=0.0,
        risk_adjustment=0.0,
        status="POSITIVE",
        reason="Confidence bound test",
    )

    result = CalibrationApplier.apply(
        score=500,
        confidence=99,
        risk=20,
        profile=profile,
    )

    assert (
        result.adjusted_confidence
        == 100.0
    )


def test_risk_lower_bound():

    profile = CalibrationProfile(
        confidence_multiplier=1.0,
        score_adjustment=0.0,
        risk_adjustment=-5.0,
        status="POSITIVE",
        reason="Risk lower bound test",
    )

    result = CalibrationApplier.apply(
        score=500,
        confidence=50,
        risk=2,
        profile=profile,
    )

    assert (
        result.adjusted_risk
        == 0.0
    )


def test_risk_upper_bound():

    profile = CalibrationProfile(
        confidence_multiplier=1.0,
        score_adjustment=0.0,
        risk_adjustment=5.0,
        status="NEGATIVE",
        reason="Risk upper bound test",
    )

    result = CalibrationApplier.apply(
        score=500,
        confidence=50,
        risk=99,
        profile=profile,
    )

    assert (
        result.adjusted_risk
        == 100.0
    )


def test_original_values_are_preserved():

    result = CalibrationApplier.apply(
        score=650,
        confidence=72,
        risk=25,
        profile=positive_profile(),
    )

    assert (
        result.original_score
        == 650.0
    )

    assert (
        result.original_confidence
        == 72.0
    )

    assert (
        result.original_risk
        == 25.0
    )


def test_to_dict():

    result = CalibrationApplier.apply(
        score=650,
        confidence=72,
        risk=25,
        profile=positive_profile(),
    )

    data = result.to_dict()

    assert (
        "original_score"
        in data
    )

    assert (
        "adjusted_score"
        in data
    )

    assert (
        "original_confidence"
        in data
    )

    assert (
        "adjusted_confidence"
        in data
    )

    assert (
        "original_risk"
        in data
    )

    assert (
        "adjusted_risk"
        in data
    )