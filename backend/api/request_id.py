from uuid import uuid4

from fastapi import Request


REQUEST_ID_HEADER = "X-Request-ID"


def get_request_id(
    request: Request,
) -> str:

    request_id = request.headers.get(
        REQUEST_ID_HEADER
    )

    if request_id:

        return request_id

    return str(uuid4())