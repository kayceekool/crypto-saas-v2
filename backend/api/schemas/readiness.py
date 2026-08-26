from pydantic import BaseModel, ConfigDict


class ReadinessResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    ready: bool
    status: str