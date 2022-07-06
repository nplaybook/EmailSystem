from pydantic import BaseModel, EmailStr, StrictStr, StrictInt, validator


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


class SMTPDetail(BaseModel):
    """Base data validation for smtp credentials"""

    email: EmailStr
    password: StrictStr
    server: StrictStr
    port: StrictInt
