from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.database import Base


class CopyTradeSignal(Base):

    __tablename__ = "copytrade_signals"

    id = Column(Integer, primary_key=True)

    wallet = Column(String)

    token = Column(String)

    action = Column(String)

    confidence = Column(Integer)