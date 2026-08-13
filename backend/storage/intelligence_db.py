from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from backend.core.database import Base


class IntelligenceRecordModel(Base):

    __tablename__ = "intelligence_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    token_address: Mapped[str] = mapped_column(
        String(255),
        index=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )

    score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    pattern: Mapped[str] = mapped_column(
        String(50),
        default="NORMAL",
    )

    risk: Mapped[str] = mapped_column(
        String(50),
        default="UNKNOWN",
    )

    signal: Mapped[str] = mapped_column(
        String(50),
        default="WATCH",
    )

    price: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    liquidity: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    volume: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    metadata_json: Mapped[str] = mapped_column(
        Text,
        default="{}",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )