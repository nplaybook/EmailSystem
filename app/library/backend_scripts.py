import os
import random
import string
from math import ceil
from subprocess import Popen, call
from datetime import datetime, timezone

from typing import BinaryIO, List, Tuple
from openpyxl import Workbook

from app.models import Email, Recipient
from app.library.const import STATUS_SENT, TO_MEGA_BYTES, ENCRYPT_SOFTWARE_DIR
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

    @staticmethod
    def remove_excel_file(base_path: str, file_name: str):
        """Remove generated xlsx file to keep the memory unoccupied
        
        :param base_path: path wehere the excel file is stored
        :param file_name: name of the file
        """

        file_path = f"{base_path}/{file_name}"
        call(f"rm '{file_path}'", shell=True)

    def save_excel_file(self, base_path: str, file_name: str, header: str, data: list):
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
    def format_base_data(header: list, data: list) -> list:
        """Change data to accepted format by xlsx
        
        :param data: data that willbe formatted
        :return: formatted data
            example - [
                [1, MoM],
                [2, MoM 2]
            ]
        """
        
        formatted_data = []
        for datum in data:
            row_data = [getattr(datum, head) for head in header]
            formatted_data.append(row_data)
        return formatted_data

    @staticmethod
    def write_data_to_excel(workbook: Workbook, header: list, data: list) -> Tuple[list, Workbook]:
        """Write data to excel
        
        :param workbook: empty workbook
        :param header: data header
        :param data: formatted data that will be written
            example - [
                [1, MoM],
                [2, MoM 2]
            ]
        """

        wb_active = workbook.active

        # add header
        wb_active.append(header)

        # insert data to excel file
        for datum in data:
            wb_active.append(datum)
        return workbook


class CommonUtils:

    def __init__():
        pass

    @staticmethod
    def measure_file_size(base_path: str, file_name: str) -> float:
        """Measure how big the size of a file

        :param base_path: base path where a specific file resides
        :param file_name: name of a file that will be measured
        """

        return os.path.getsize(f"{base_path}/{file_name}") / TO_MEGA_BYTES  # bytes to mbs

    @staticmethod
    def generate_password() -> str:
        """Generate ASCII characters for protecting a file.
        Password should be: alphabet uppercase, alphabet lowecase, and digits.
        Password length will be 8 characters long

        :return: generated ASCII password
        """

        return ''.join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            ) for _ in range(8)
        )

    @staticmethod
    def encrypt_file(base_path: str, file_name: str, password: str) -> BinaryIO:
        """Encrypt an unencrypted file

        :param base_path: base path where the file resides
        :param file_name: name of a file
        :param password: keyphrase that will be used to open the encrypted file
        :return: file contents of encrypted file
        """

        # unencryted file structure: xxx - xxx.ext
        # encrypted file structure: xxx.xxx.ext
        unencrypted_file_path = f"{base_path}/{file_name}"
        encrypted_file_path = f"{base_path}/{file_name.replace('_', '.')}"

        # refer to https://github.com/herumi/msoffice#how-to-use for encrypption lib details
        encryption_status = Popen(
                f'bin/msoffice-crypt.exe -e -p {password} "{unencrypted_file_path}" "{encrypted_file_path}"',
                cwd=ENCRYPT_SOFTWARE_DIR,
                shell=True
            )

        # encryption status possibility:
        # 0: success; 1: not support format; 2: already encrypted with -e or decrypted with -d
        # 3: bad password with -d
        if encryption_status.wait() == 0:
            with open(encrypted_file_path, "rb") as encrypted_file:
                return encrypted_file.read()
        return

    # TODO: might want to move to excel handler -> and other methods below
    @staticmethod
    def count_split(file_size: float, max_size: int) -> int:
        """Calculate how many files that a file need to be splitted.

        :param file_size: size of a file
        :param max_size: maximum size of a file
        :return: total number of splitted file
        """

        return ceil(file_size/max_size)

    @staticmethod
    def split_file(file_name: str, num_of_split: int, ext: str) -> List:
        """Split size if the data more than certain amount of size by `max_size`
        
        :param file_name: name of a file that will be splitted
        :param num_of_split: expected number of total files after splitted
        :param ext: file extension
        :return: list of filenames
        """

        files = []
        for split in range(num_of_split):
            splitted_file_name = f"{file_name}-part-{split+1}.{ext}"
            files.append(splitted_file_name)
        return files

    @staticmethod
    def get_data_index(data: list, part: int, data_per_part: int) -> tuple:
        """A method to get data index specifically for parted files

        :param data: formatted data that will be written
            example - [
                [1, MoM],
                [2, MoM 2]
            ]
        :param part: on which part the data will be used
        :param data_per_part: how many data will be stored per file/part:
        :return: start index and end index for specific data part
        """

        if part == 1:
            start_range = 1
            end_range = start_range + data_per_part
        else:
            start_range = (data_per_part * (part-1)) + part
            end_range = min(start_range + data_per_part, len(data))
        return start_range, end_range
