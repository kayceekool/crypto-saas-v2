from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from core.database import Base


class Token(Base):

    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True
    )

    symbol = Column(
        String
    )

    address = Column(
        String
    )

    price = Column(
        Float
    )

    liquidity = Column(
        Float
    )

    volume = Column(
        Float
    )

    market_cap = Column(
        Float
    )

    score = Column(
        Float
    )

    confidence = Column(
        Float
    )

    risk = Column(
        String
    )

    signal = Column(
        String
    )

    rating = Column(
        String
    )

    age_hours = Column(
        Float
    )

    wallet_interest = Column(
        Float
    )

    migration_score = Column(
        Float
    )

    launch_score = Column(
        Float
    )

    last_seen = Column(
        String
    )