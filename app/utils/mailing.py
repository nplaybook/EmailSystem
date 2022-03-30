import smtplib, ssl
from pytz import timezone
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app import scheduler
from app.db import Session, engine
from app.models import Email
from app.config.config import (
    EMAIL, PASSWORD, 
    SMTP_PORT, SMTP_SERVER, 
    STATUS_PENDING, STATUS_SENT
)


def send_email(email_attribute: Email) -> None:
    """Send email using smtp
    
    :param email_id: id will be used to query sender, reciever, and email
    content
    """

    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        # connect to server and loging
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        recipients = [recipient.to_email for recipient in email_attribute.recipients]
        
        # prepare email content
        message = MIMEMultipart()
        message["Subject"] = email_attribute.email_subject
        message["From"] = email_attribute.from_email
        message["To"] = ", ".join(recipients)
        body = MIMEText(email_attribute.email_content)
        message.attach(body)

        # send email
        server.sendmail(message["From"], recipients, message.as_string())

@scheduler.task("interval", id="scheduled-email", seconds=15)
def check_scheduled_email() -> None:
    """Cron job function to check scheduled email that remain pending.
    Will check on specific interval."""

    print(f"Cron jon run at {datetime.now()}")

    with Session(bind=engine) as session:
        emails = session.query(Email).\
            filter(Email.status == STATUS_PENDING, 
            Email.schedule_at <= datetime.now(timezone("Asia/Singapore"))
            ).\
            all()
    
        for email in emails:
            send_email(email_attribute=email)
            session.query(Email).\
                filter(Email.id == email.id).\
                update({"status": STATUS_SENT})
            session.commit()

    print(f"Cron jon finish at {datetime.now()}")