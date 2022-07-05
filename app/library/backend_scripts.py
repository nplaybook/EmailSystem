from typing import Dict, NoReturn
from datetime import datetime, timezone


class EmailHandler:
    """EmailHandler responsible to handle generic operation related to email.

    :param table_name: name of the table that is requested to sent
    :param file_name: file name that will be sent through email
    """

    def __init__(self, table_name: str, file_name: str):
        """Constructor for EmailHandler
        
        :param table_name: name of the table that is requested to sent
        :param file_name: file name that will be sent through email
        """

        self.table_name = table_name
        self.file_name = file_name

    def get_email_metadata(self) -> Dict[str, str]:
        """Control flow to select which metadata details to used for sending
        email.

        :param table: name of the table that is requested by client
        :return: dictionary of necessary element to send an email
        """

        email_subject: dict = {
            "event": "Available Events",
            "email-provider": "Listed Email Providers"
        }

        email_body: dict = {
            "event": """
                Here are the list of available events for our system per this
                email is sent.
            """,
            "email-providers": """
                Here are the list of email providers that has made an agreement
                with us.
            """
        }

        return {
            "subject": email_subject[self.table_name],
            "body": email_body[self.table_name]
        }


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