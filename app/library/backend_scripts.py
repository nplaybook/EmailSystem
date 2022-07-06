from typing import NoReturn, List
from datetime import datetime, timezone
from app.library.const import STATUS_SENT
from app.library.typing import DB_SESSION

from app.models import Email, Recipient


class DBEmailTransaction:

    def __init__(self, email: Email) -> NoReturn:
        self.email = email

    def insert_email_record(self, db: DB_SESSION) -> NoReturn:
        """Insert email detail to database and assign attribute
        email id to class

        :param db: database session from Flask g variable
        """

        db.add(self.email)
        db.commit()
        db.flush()
        self.email_id = self.email.id

    def insert_recipient_record(
        self,
        db: DB_SESSION,
        recipients: List[Recipient]
    ) -> NoReturn:
        """Insert recipient data from `to_email` key

        :param db: database session from Flask g variable
        """

        db.add_all(recipients)
        db.commit()

    def update_email_status(self, db: DB_SESSION) -> NoReturn:
        """Update email status to SENT or FAIL

        :param db: database session in Flask g variable
        """

        db.query(Email)\
            .filter(Email.id == self.email_id)\
            .update({"status": STATUS_SENT})
        db.commit()


class ExcelFileHandler:
    """ExcelFileHandler responsible to handle generic functionality of operations
    related to excel file.

    :param table_name (str): name of the table that will be exported
    """

    def __init__(self, table_name: str) -> NoReturn:
        """Constructor for ExcelFileHandler

        :param table_name (str): name of the table taht will be exported
        """

        self.table_name = table_name

    def generate_filename(self) -> str:
        """Auto generate excel filename following specific format

        :param table: name of the table that will be reported
        :return: auto generated excel filename
        """

        time_generated = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M")
        return f"{self.table_name} - {time_generated}.xlsx"

    def remove_existing_excel_file(self, base_path: str) -> NoReturn:
        pass

    def generate_excel_file(self, base_path: str):
        pass
