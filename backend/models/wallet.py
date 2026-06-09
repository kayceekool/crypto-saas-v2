from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from core.database import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(
        Integer,
        primary_key=True
    )

    wallet = Column(
        String,
        unique=True
    )

    total_trades = Column(
        Integer,
        default=0
    )

    winning_trades = Column(
        Integer,
        default=0
    )

    losing_trades = Column(
        Integer,
        default=0
    )

    win_rate = Column(
        Float,
        default=0
    )

    roi = Column(
        Float,
        default=0
    )

    score = Column(
        Float,
        default=0
    )

    rank = Column(
        String,
        default="UNRANKED"
    )

    last_seen = Column(
        String
    )

    followed = Column(
        Integer,
        default=0
    )

    copytrade_enabled = Column(
        Integer,
        default=0
    )

    smart_wallet = Column(
        Integer,
        default=0
    )