from typing import List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class EmailBase(BaseModel):
    event_id: int
    email_subject: str
    email_content: str
    from_email: EmailStr 
    schedule_at: datetime = Field(alias="timestamp")

    class Config:
        orm_mode = True


class SaveEmailPayload(EmailBase):
    to_email: List[EmailStr]