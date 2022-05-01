# sourcery skip: avoid-builtin-shadow
from sqlalchemy import Column, Integer, String

from .base import Base


class Provider(Base):
    __tablename__ = "email_provider"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    domain = Column(String(32))
    server = Column(Integer)
    port = Column(String)
