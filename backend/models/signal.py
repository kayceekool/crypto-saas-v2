from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from core.database import Base


class Signal(Base):

    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)

    signal = Column(String)

    confidence = Column(Float)

    score = Column(Float)

    timestamp = Column(String)