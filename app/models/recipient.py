# sourcery skip: avoid-builtin-shadow
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from .base import Base


class Recipient(Base):
    __tablename__ = "recipients"
    id = Column(Integer, primary_key=True, nullable=False)
    email_id = Column(Integer, ForeignKey("emails.id"))
    to_email = Column(String)
    created_at = Column(DateTime, default=datetime.now)    
