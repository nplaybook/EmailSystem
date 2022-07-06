from typing import Literal
from pydantic import BaseModel

from app.schemas.base import SMTPDetail


class ExportReportPayload(BaseModel):
    """Base model validation for export data"""

    smtp: SMTPDetail
    report: Literal["event", "email-provider"]
