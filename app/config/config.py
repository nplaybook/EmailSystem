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

INSERT_STATUS = os.environ.get("INSERT_STATUS")
FAIL_STATUS = os.environ.get("FAIL_STATUS")
SUCCESS_STATUS = os.environ.get("SUCCESS_STATUS")

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_SERVER = os.environ.get("SMTP_SERVER")