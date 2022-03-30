import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import Email
from app.config.config import EMAIL, PASSWORD, SMTP_PORT, SMTP_SERVER


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