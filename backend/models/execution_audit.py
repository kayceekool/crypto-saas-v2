from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base


class ExecutionAudit(Base):
    __tablename__ = "execution_audits"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    decision: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    gate_approved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    execution_enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    executed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    dry_run: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(
            timezone.utc
        ),
    )