import os
from ast import literal_eval
from dotenv import load_dotenv

load_dotenv(".env")


SECRET_KEY = os.environ.get("SECRET_KEY")

DB_BASE_DIR = os.environ.get("DB_BASE_DIR")
DB_DIALECT = os.environ.get("DB_DIALECT")
DB_NAME = os.environ.get("DB_NAME")

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = literal_eval(os.environ.get("CELERY_ACCEPT_CONTENT"))
CELERY_RESULT_SERIALIZER = os.environ.get("CELERY_RESULT_SERIALIZER")
CELERY_TASK_SERIALIZER = os.environ.get("CELERY_TASK_SERIALIZER")

PAYLOAD_EMAIL = ["event_id", "from_email", "email_subject", "email_content", "schedule_at"]
PAYLOAD_RECIPIENT = "to_email"

STATUS_PENDING = "PENDING"
FAIL_STATUS = "FAILED"
STATUS_SENT = "SENT"

SCHEDULE_LIMIT = 60 * 2
