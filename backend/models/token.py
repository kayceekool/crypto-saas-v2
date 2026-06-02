from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from core.database import Base


class Token(Base):

    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)

    address = Column(String)

    price = Column(Float)

    liquidity = Column(Float)

    volume = Column(Float)

    market_cap = Column(Float)

    score = Column(Float)

    risk = Column(String)

    confidence = Column(Float)

    signal = Column(String)