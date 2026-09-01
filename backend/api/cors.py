from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)


def configure_cors(
    app: FastAPI,
    origins: str,
) -> None:

    allowed_origins = [
        origin.strip()
        for origin in origins.split(",")
        if origin.strip()
    ]

    if not allowed_origins:

        allowed_origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=(
            "*" not in allowed_origins
        ),
        allow_methods=["*"],
        allow_headers=["*"],
    )