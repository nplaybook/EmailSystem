from typing import Optional
from pydantic import BaseModel, EmailStr, Literal
from datetime import datetime


class EmailBase(BaseModel):
    id: int
    subject: str
    content: str
    from_email: EmailStr
    schedule_at: datetime
    status: Literal["Pending", "Sent", "Failed"]
    created_at: Optional[datetime] = []
    updated_at: Optional[datetime] = []

    class Config:
        orm_mode = True


class EmailCreate(EmailBase):
    pass


class EmailUpdate(EmailBase):
    status: str