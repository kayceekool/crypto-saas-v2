from typing import Any

from pydantic import BaseModel, ConfigDict


class HealthComponent(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    status: str
    detail: str
    updated_at: str


class HealthResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    status: str
    components: dict[str, HealthComponent]