import pytest

from pydantic import ValidationError

from backend.api.schemas.errors import (
    ErrorResponse,
)


def test_valid_error_response():

    result = ErrorResponse(
        error="backend_unavailable",
        message="Backend is unavailable.",
    )

    assert (
        result.error
        == "backend_unavailable"
    )

    assert (
        result.message
        == "Backend is unavailable."
    )


def test_error_response_serializes():

    result = ErrorResponse(
        error="invalid_request",
        message="Request is invalid.",
    )

    data = result.model_dump()

    assert data == {
        "error": "invalid_request",
        "message": "Request is invalid.",
    }


def test_extra_fields_are_rejected():

    with pytest.raises(
        ValidationError
    ):

        ErrorResponse(
            error="test",
            message="Test message.",
            unexpected="bad",
        )


def test_missing_error_is_rejected():

    with pytest.raises(
        ValidationError
    ):

        ErrorResponse(
            message="Test message.",
        )


def test_missing_message_is_rejected():

    with pytest.raises(
        ValidationError
    ):

        ErrorResponse(
            error="test",
        )


def test_empty_strings_are_allowed():

    result = ErrorResponse(
        error="",
        message="",
    )

    assert result.error == ""
    assert result.message == ""