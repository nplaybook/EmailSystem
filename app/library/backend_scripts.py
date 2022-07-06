from typing import List
from datetime import datetime, timezone

from openpyxl import Workbook

from app.models import Email, Recipient
from app.library.const import STATUS_SENT
from app.library.typing import DB_SESSION


class DBEmailTransaction:

    def __init__(self):
        pass

    def insert_email_record(self, db: DB_SESSION, email: Email) -> int:
        """Insert email detail to database and assign attribute
        email id to class

        :param db: database session from Flask g variable
        :param email: Email object that will be recorded
        :return: email id
        """

        db.add(email)
        db.commit()
        db.flush()
        self.email_id = email.id

    def insert_recipient_record(self, db: DB_SESSION, recipients: List[Recipient]):
        """Insert recipient data from `to_email` key

        :param db: database session from Flask g variable
        """

        db.add_all(recipients)
        db.commit()

    def update_email_status(self, db: DB_SESSION, email_id: int):
        """Update email status to SENT or FAIL

        :param db: database session in Flask g variable
        :param email_id: email ID
        """

        db.query(Email)\
            .filter(Email.id == email_id)\
            .update({"status": STATUS_SENT})
        db.commit()


class ExcelFileHandler:
    """ExcelFileHandler responsible to handle generic functionality of operations
    related to excel file.

    :param table_name (str): name of the table that will be exported
    """

    def __init__(self, table_name: str):
        """Constructor for ExcelFileHandler

        :param table_name (str): name of the table taht will be exported
        """

        self.table_name = table_name

    def generate_filename(self, time_format: str, ext: str) -> str:
        """Auto generate excel filename following specific format

        :param format: desired time format
        :param ext: file extension
        :return: auto generated excel filename
        """

        time_generated = datetime.now(timezone.utc).strftime(time_format)
        return f"{self.table_name} - {time_generated}.{ext}"

    def remove_existing_excel_file(self, base_path: str):
        pass

    def generate_excel_file(self, base_path: str, file_name: str, header: str, data: list) -> Workbook:
        """Generate new excel file
        
        :param base_path: path where the excel file will be stored
        :param file_name: name of the file
        :param header: data header
        :param data: data that will be written to the excel file
        :return: excel Workbook
        """

        workbook = Workbook()
        workbook = self.write_data_to_excel(workbook, header, data)
        workbook.save(f"{base_path}/{file_name}")

    @staticmethod
    def write_data_to_excel(workbook: Workbook, header: list, data: list) -> Workbook:
        """Write data to excel
        
        :param workbook: empty workbook
        :param header: data header
        :param data: data that will be written
        """

        wb_active = workbook.active

        # add header
        wb_active.append(header)

        # format data dynamically following available header
        formatted_data = []
        for datum in data:
            row_data = [getattr(datum, head) for head in header]
            formatted_data.append(row_data)

        # insert data to excel file
        for datum in formatted_data:
            wb_active.append(datum)

        return workbook
