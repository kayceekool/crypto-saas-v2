from pydantic import BaseModel, ConfigDict


class StatusResponse(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    name: str
    version: str
    status: str
    ready: bool
    lifecycle: str