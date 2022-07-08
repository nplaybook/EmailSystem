from typing import List, Dict, Optional

import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# from app.app import celery
from app.models import Email, Recipient
# from app.library.celery_sqlalchemy import SQLAlchemyTask
from app.library.const import PAYLOAD_EMAIL, STATUS_PENDING
from app.library.typing import JSON, DB_SESSION


class EmailOps:

    def __init__(self, payload: JSON):
        """Initialize EmailUtils class which handle all the operations
        necessary to send email.

        :param payload: from validated request.json
            example - {
                "smtp": {
                    "server": ...,
                    "port": ...,
                    "email": ...,
                    "password": ...
                }
                "email": {
                    "email_subject": subject,
                    "email_content": content,
                    "email_attachment": attachment file  # optional
                    "email_attachment_name": attachment name  # optional
                    "from_email": ...,
                    "to_email": [..., ...]                    
                }
            }
        """

        self.smtp = payload["smtp"]
        self.email = payload["email"]

    def send_email(self, db: DB_SESSION, type: str):  # sourcery skip: remove-redundant-if
        """Send email functionality
        
        :param db: database session from Flask g variable, used to update email record
        :param type: type of email that will be sent
            example - plain, html
        :return: detail of the sending message process
        """
        context = ssl.create_default_context()
        
        # prepare email content
        message = MIMEMultipart()
        message["Subject"] = self.email["email_subject"]
        message["From"] = self.email["from_email"]
        recipients = self.email["to_email"]
        message["To"] = ", ".join(recipients)
        body = MIMEText(self.email["email_content"], type)
        message.attach(body)

        # if any attachment
        if "email_attachment" and "email_attachment_name" in self.email:
            attachment = MIMEApplication(self.email["email_attachment"], Name=self.email["email_attachment_name"])
            attachment["Content Disposition"] = f"attachment; filename={self.email['email_attachment_name']}"
            message.attach(attachment)

        with smtplib.SMTP(self.smtp["server"], self.smtp["port"]) as server:
            # connect and login to email provider
            server.starttls(context=context)
            server.login(self.smtp["email"], self.smtp["password"])
            # send email
            server.sendmail(message["From"], recipients, message.as_string())

            # update email status
            # TODO: get celery status then update email status
            # self.update_email_status(db)


class EmailPrep:

    def __init__(self, email: Email, table_report: Optional[str]=None):
        """Class initiator

        :param email: email payload from request.json
        :param table_name: name of the requested table report (optional)
        """
        self.email = email
        if table_report:
            self.table_report = table_report

    def format_recipient_data(self, email_id: int, key: str = "to_email") -> List[Recipient]:
        """Format list of recipient email to JSON ARRAY format
        that is accepted by Recipient object

        :param email_id: email ID
        :param key: payload key that contains to_email data
        :return: JSON ARRAY of Recipient model
        """

        to_email = self.email[key]
        recipients = [
            {"email_id": email_id, "to_email": email} for email in to_email
        ]
        return [Recipient(**recipient) for recipient in recipients]

    def assign_pending_status(self) -> Email:
        """Add email status as pending and format data to Email model

        :return: Email model
        """

        email = {key: self.email[key] for key in PAYLOAD_EMAIL}
        email["status"] = STATUS_PENDING
        return Email(**email)

    def get_email_metadata(
        self,
        attachment_filename: str,
        password: str,
        part: Optional[str]=None,
        total_part: Optional[str]=None
    ) -> Dict[str, str]:
        """Control flow to select which metadata details to used for sending
        email.

        :param attachment_filename: name of the attachment file
        :param passsword: password that will be used to open the attachment file
        :param part: current part if file are divided to several parts otherwise None
        :param total_part: total part if file are divided to several parts otherwise None
        :return: dictionary of necessary element to send an email
            example - {
                "subject": "Available events",
                "body": "Here are the list of available events"
            }
        """

        base_message = f"""
        For security purpose, we have locked the attached file. <br>
        You can use following password <strong>{password}</strong> to unlock the file. <br>
        Should you have any questions regarding the report, please approach the owner. <br><br>
        Thank you, <br>
        Someone else <br>
        <i>P.S. This email is automatically generated. Please do not reply to this email.</i>
        """

        if part and total_part:
            subject = {
                "event": f"Available Events (part {part}/{total_part})",
                "email-provider": f"Listed Email Providers (part {part}/{total_part})"
            }

            message = f""""
            This is the data which you have requested.
            This dataset includes all {self.table_report} records information. <br>
            We have splitted the report to smaller files to avoid hitting the maximumum attachment size.
            This is {part}/{total_part} part reports.
            """
        else:
            subject = {
                "event": "Available Events ",
                "email-provider": "Listed Email Providers"
            }

            message = f"""
            This is the data which you have been requested. <br>
            This dataset includes all {self.table_report} records information.
            """

        message = f"{message} <br><br> {base_message}"

        return {
            "subject": subject[self.table_report],
            "body": message,
            "attachment_filename": attachment_filename
        }


# @celery.task(base=SQLAlchemyTask, max_retries=5, default_retry_delay=15)
def send_email_task(db: DB_SESSION, payload: JSON, type: str="plain"):
    """send_email method wrapper to prevent passing self argument as 
    an actual argument instead of self-referencing (due to celery.task)

    :param db: database session from Flask g
    :param payload: data/information that will be processed upon request
    :param type: type of email that will be sent
        example: plain, html
    """

    e = EmailOps(payload)
    e.send_email(db, type)


# @celery.task(base=SQLAlchemyTask, max_retries=5, default_retry_delay=15)
# def test_celery() -> NoReturn:
#     print("SUCCESS")
