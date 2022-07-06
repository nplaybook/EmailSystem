from typing import List
from datetime import datetime
from pydantic import (
    BaseModel, EmailStr, Field, validator
)

from app.schemas.base import EmailDetail, SMTPDetail
from app.library.const import SCHEDULE_LIMIT


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
