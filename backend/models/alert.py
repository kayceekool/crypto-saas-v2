from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from core.database import Base


class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    level = Column(String)

    title = Column(String)

    message = Column(String)

    timestamp = Column(String)