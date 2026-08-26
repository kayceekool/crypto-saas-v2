from pydantic import BaseModel, ConfigDict, Field


class ExecutionMonitoringSummaryResponse(
    BaseModel
):
    model_config = ConfigDict(
        extra="forbid"
    )

    total: int = Field(
        ge=0
    )

    accepted: int = Field(
        ge=0
    )

    rejected: int = Field(
        ge=0
    )

    watched: int = Field(
        ge=0
    )

    strong: int = Field(
        ge=0
    )

    gate_approved: int = Field(
        ge=0
    )

    gate_blocked: int = Field(
        ge=0
    )

    executed: int = Field(
        ge=0
    )

    dry_run: int = Field(
        ge=0
    )

    acceptance_rate: float = Field(
        ge=0.0,
        le=1.0,
    )

    execution_rate: float = Field(
        ge=0.0,
        le=1.0,
    )

    dry_run_rate: float = Field(
        ge=0.0,
        le=1.0,
    )