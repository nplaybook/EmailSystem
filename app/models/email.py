# sourcery skip: avoid-builtin-shadow
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    subject = Column(String)
    content = Column(String)
    from_email = Column(String)
    schedule_at = Column(DateTime)
    status = Column(String(16))
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    recipients = relationship("Recipient")