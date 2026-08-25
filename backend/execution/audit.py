from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ExecutionAuditRecord:
    """
    Immutable audit record for an execution decision.

    Package 21 records decisions only.
    It does not execute transactions.
    """

    decision: str
    score: float
    confidence: float
    risk: float

    gate_approved: bool
    execution_enabled: bool

    executed: bool
    dry_run: bool

    message: str
    created_at: datetime

    @classmethod
    def from_execution(
        cls,
        *,
        decision: str,
        score: float,
        confidence: float,
        risk: float,
        gate_approved: bool,
        execution_enabled: bool,
        executed: bool,
        dry_run: bool,
        message: str,
    ) -> "ExecutionAuditRecord":

        return cls(
            decision=decision,
            score=float(score),
            confidence=float(confidence),
            risk=float(risk),
            gate_approved=bool(gate_approved),
            execution_enabled=bool(
                execution_enabled
            ),
            executed=bool(executed),
            dry_run=bool(dry_run),
            message=message,
            created_at=datetime.now(
                timezone.utc
            ),
        )

    def to_dict(self) -> dict:
        return {
            "decision": self.decision,
            "score": self.score,
            "confidence": self.confidence,
            "risk": self.risk,
            "gate_approved": self.gate_approved,
            "execution_enabled": (
                self.execution_enabled
            ),
            "executed": self.executed,
            "dry_run": self.dry_run,
            "message": self.message,
            "created_at": (
                self.created_at.isoformat()
            ),
        }