from typing import List, Dict

import ssl
import smtplib
from email.mime.text import MIMEText
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
        """

        self.smtp = payload["smtp"]
        self.email = payload["email"]

    def send_email(self, db: DB_SESSION):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp["server"], self.smtp["port"]) as server:
            # connect and login to email provider
            server.starttls(context=context)
            server.login(self.smtp["email"], self.smtp["password"])

            # prepare email content
            message = MIMEMultipart()
            message["Subject"] = self.email["email_subject"]
            message["From"] = self.email["from_email"]
            recipients = self.email["to_email"]
            message["To"] = ", ".join(recipients)
            body = MIMEText(self.email["email_content"])
            message.attach(body)

            # send email
            server.sendmail(message["From"], recipients, message.as_string())

            # update email status
            # TODO: get celery status then update email status
            # self.update_email_status(db)
            # print("===========DONE=============")


class EmailPrep:

    def __init__(self, email: Email):
        self.email = email

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


# @celery.task(base=SQLAlchemyTask, max_retries=5, default_retry_delay=15)
def send_email_task(db: DB_SESSION, payload: JSON):
    """send_email method wrapper to prevent passing self argument as 
    an actual argument instead of self-referencing (due to celery.task)
    """

    e = EmailOps(payload)
    e.send_email(db)


# @celery.task(base=SQLAlchemyTask, max_retries=5, default_retry_delay=15)
# def test_celery() -> NoReturn:
#     print("SUCCESS")
