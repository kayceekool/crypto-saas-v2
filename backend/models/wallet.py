from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from core.database import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)

    wallet = Column(String, unique=True)

    total_trades = Column(Integer, default=0)

    winning_trades = Column(Integer, default=0)

    losing_trades = Column(Integer, default=0)

    win_rate = Column(Float, default=0)

    roi = Column(Float, default=0)

    score = Column(Float, default=0)

    rank = Column(String, default="UNRANKED")