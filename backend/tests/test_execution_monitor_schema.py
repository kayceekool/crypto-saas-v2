from pydantic import ValidationError

import pytest

from backend.api.schemas.execution_monitor import (
    ExecutionMonitoringSummaryResponse,
)


def make_valid_data():

    return {
        "total": 10,
        "accepted": 3,
        "rejected": 2,
        "watched": 2,
        "strong": 3,
        "gate_approved": 6,
        "gate_blocked": 4,
        "executed": 0,
        "dry_run": 10,
        "acceptance_rate": 0.6,
        "execution_rate": 0.0,
        "dry_run_rate": 1.0,
    }


def test_valid_summary_is_accepted():

    result = (
        ExecutionMonitoringSummaryResponse(
            **make_valid_data()
        )
    )

    assert result.total == 10
    assert result.accepted == 3
    assert result.strong == 3
    assert result.executed == 0
    assert result.dry_run == 10


def test_negative_total_is_rejected():

    data = make_valid_data()

    data["total"] = -1

    with pytest.raises(
        ValidationError
    ):

        ExecutionMonitoringSummaryResponse(
            **data
        )


def test_negative_execution_count_is_rejected():

    data = make_valid_data()

    data["executed"] = -1

    with pytest.raises(
        ValidationError
    ):

        ExecutionMonitoringSummaryResponse(
            **data
        )


def test_rate_above_one_is_rejected():

    data = make_valid_data()

    data["acceptance_rate"] = 1.1

    with pytest.raises(
        ValidationError
    ):

        ExecutionMonitoringSummaryResponse(
            **data
        )


def test_rate_below_zero_is_rejected():

    data = make_valid_data()

    data["dry_run_rate"] = -0.1

    with pytest.raises(
        ValidationError
    ):

        ExecutionMonitoringSummaryResponse(
            **data
        )


def test_unexpected_field_is_rejected():

    data = make_valid_data()

    data["unexpected"] = "bad"

    with pytest.raises(
        ValidationError
    ):

        ExecutionMonitoringSummaryResponse(
            **data
        )


def test_schema_serializes_cleanly():

    result = (
        ExecutionMonitoringSummaryResponse(
            **make_valid_data()
        )
    )

    data = result.model_dump()

    assert data["total"] == 10
    assert data["acceptance_rate"] == 0.6
    assert data["execution_rate"] == 0.0
    assert data["dry_run_rate"] == 1.0