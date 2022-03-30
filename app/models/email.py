# sourcery skip: avoid-builtin-shadow
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    email_subject = Column(String, nullable=False)
    email_content = Column(String, nullable=False)
    from_email = Column(String, nullable=False)
    schedule_at = Column(DateTime, nullable=False)
    status = Column(String(16), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    recipients = relationship("Recipient", lazy='subquery')