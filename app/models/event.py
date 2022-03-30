# sourcery skip: avoid-builtin-shadow
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    emails = relationship("Email")