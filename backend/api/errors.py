from fastapi import Request
from fastapi.responses import JSONResponse

from backend.api.schemas.errors import (
    ErrorResponse,
)


class APIError(Exception):

    def __init__(
        self,
        error: str,
        message: str,
        status_code: int = 400,
    ) -> None:

        self.error = error
        self.message = message
        self.status_code = status_code

        super().__init__(message)


async def api_error_handler(
    request: Request,
    exc: APIError,
) -> JSONResponse:

    payload = ErrorResponse(
        error=exc.error,
        message=exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=payload.model_dump(),
    )