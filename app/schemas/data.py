from typing import Literal
from pydantic import BaseModel


class ExportReport(BaseModel):
    """Base model validation for export data"""

    table: Literal["event", "email-provider"]
