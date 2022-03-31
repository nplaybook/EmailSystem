import os
from dotenv import load_dotenv

load_dotenv(".env")

SECRET_KEY = os.environ.get("SECRET_KEY")

DB_DIALECT = os.environ.get("DB_DIALECT")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

PAYLOAD_EMAIL = os.environ.get("PAYLOAD_EMAIL")
PAYLOAD_RECIPIENT = os.environ.get("PAYLOAD_RECIPIENT")

STATUS_PENDING = os.environ.get("STATUS_PENDING")
FAIL_STATUS = os.environ.get("FAIL_STATUS")
STATUS_SENT = os.environ.get("STATUS_SENT")

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
SMTP_PORT = int(os.environ.get("SMTP_PORT"))
SMTP_SERVER = os.environ.get("SMTP_SERVER")

SCHEDULE_LIMIT = eval(os.environ.get("SCHEDULE_LIMIT"))

CRON_INTERVAL = int(os.environ.get("CRON_INTERVAL"))