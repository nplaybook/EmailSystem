from typing import List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.types import constr

class EmailBase(BaseModel):
    event_id: int
    email_subject: str
    email_content: str
    from_email: EmailStr 


    @validator("email_subject")
    def check_email_subject(cls, v):
        assert v != "", "Empty subject is not allowed"
        return v


    @validator("email_content")
    def check_email_content(cls, v):
        assert v != "", "Empty content is not allowed"
        return v


class SaveEmailPayload(EmailBase):
    to_email: List[EmailStr]
    schedule_at: datetime = Field(alias="timestamp")