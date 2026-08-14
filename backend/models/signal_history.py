from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from backend.core.database import Base


class SignalHistory(Base):

    __tablename__ = "signal_history"

    id = Column(Integer, primary_key=True)

    token = Column(String)

    signal = Column(String)

    score = Column(Float)

    confidence = Column(Float)

    price_at_signal = Column(Float)

    outcome = Column(String)

    pnl = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )