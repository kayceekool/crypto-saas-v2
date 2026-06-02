from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from core.database import Base


class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)

    wallet = Column(String)

    win_rate = Column(Float)

    roi = Column(Float)

    score = Column(Float)

    rank = Column(String)