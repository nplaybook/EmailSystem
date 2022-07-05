from typing import List
from datetime import datetime
from pydantic import (
    BaseModel, StrictStr, StrictInt, EmailStr,
    Field, validator
)

from app.library.const import SCHEDULE_LIMIT


class SMTPDetail(BaseModel):
    """Base data validation for smtp credentials"""

    email: EmailStr
    password: StrictStr
    server: StrictStr
    port: StrictInt


class EmailDetail(BaseModel):
    """Base data validation for table Email"""

    event_id: int
    email_subject: StrictStr
    email_content: StrictStr
    from_email: EmailStr


    @validator("email_subject")
    @classmethod
    def check_email_subject(cls, v):
        assert v != "", "Empty subject is not allowed"
        return v

    @validator("email_content")
    @classmethod
    def check_email_content(cls, v):
        assert v != "", "Empty content is not allowed"
        return v


class SendDirectly(EmailDetail):
    """Use to validate send_directly payload"""
    to_email: List[EmailStr]


class SendLater(EmailDetail):
    """Use to validate send_later payload"""

    to_email: List[EmailStr]
    schedule_at: datetime = Field(alias="timestamp")


    @validator("schedule_at", pre=True)
    @classmethod
    def change_format_to_datetime(cls, v):
        try:
            return datetime.strptime(v, "%d %b %Y %H:%M")
        except ValueError as e:
            raise ValueError("Incorrect date format, should be %d %b %Y %H:%M") from e

    @validator("schedule_at")
    @classmethod
    def check_schedule_at(cls, v):
        """Difference comparison in seconds"""

        time_difference = (datetime.now() - v).total_seconds()
        assert time_difference < SCHEDULE_LIMIT, "Schedule is not valid"
        return v


class EmailDirectlyPayload(BaseModel):
    smtp: SMTPDetail
    email: SendDirectly


class EmailLaterPayload(BaseModel):
    smtp: SMTPDetail
    email: SendLater
