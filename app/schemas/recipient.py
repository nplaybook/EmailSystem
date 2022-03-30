from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class RecipientBase(BaseModel):
    id: int
    email_id: int
    to_email: EmailStr
    created_at: Optional[datetime] = []

    class Config:
        orm_mode = True


class RecipientCreate(RecipientBase):
    pass