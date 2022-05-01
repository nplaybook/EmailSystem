from typing import NoReturn, List

import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import Base, Email, Recipient
from app.config.config import PAYLOAD_EMAIL, STATUS_PENDING, STATUS_SENT
from app.library.typing import JSON, DB_SESSION


class EmailUtils:

    def __init__(self, payload: JSON) -> NoReturn:
        """Initialize EmailUtils class which handle all the operations
        necessary to send email.

        :param payload: from validated request.json
        """

        self.smtp = payload["smtp"]
        self.email = payload["email"]

    # TODO: include this in CELERY
    def send_email(self, db: DB_SESSION) -> NoReturn:
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
            self.update_email_status(db)

    def insert_email_record(self, db: DB_SESSION) -> int:
        """Insert email detail to database

        :param db: database `session` in Flask g variable
        """

        email = self._format_email_data()
        db.add(email)
        db.commit()
        db.flush()
        self.email_id = email.id

    def _format_email_data(self) -> Base:
        """Format data to SQLAlchemy Email model

        :return: data to insert in SQLAlchemy Email model
        """

        email = {key: self.email[key] for key in PAYLOAD_EMAIL}
        email["status"] = STATUS_PENDING
        return Email(**email)

    def insert_recipient_record(
        self,
        db: DB_SESSION,
    ) -> NoReturn:
        """"Insert recipient data from `to_email` key from payload
        request.

        :param db: database `session` in Flask g variable
        """

        recipients = self._format_recipient_data()
        db.add_all(recipients)
        db.commit()

    def _format_recipient_data(self, key: str = "to_email") -> List[Base]:
        """Format list of recipient email to JSON ARRAY format
        that is accepted by Recipient object

        :param key: payload key that contains to_email data
        :return: JSON ARRAY of Recipient SQLAlchemy model
        """

        to_email = self.email[key]
        recipients = [
            {"email_id": self.email_id, "to_email": email} for email in to_email
            ]
        return [Recipient(**recipient) for recipient in recipients]

    def update_email_status(self, db: DB_SESSION) -> NoReturn:
        """Update email status to SENT or FAIL

        :param db: database `session` in Flask g variable
        """

        db.query(Email).\
            filter(Email.id == self.email_id).\
            update({"status": STATUS_SENT})
        db.commit()
