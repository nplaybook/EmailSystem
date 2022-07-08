import os

# Email essentials
PAYLOAD_EMAIL = ["event_id", "from_email", "email_subject", "email_content", "schedule_at"]
PAYLOAD_RECIPIENT = "to_email"

# Email send status
STATUS_PENDING = "PENDING"
FAIL_STATUS = "FAILED"
STATUS_SENT = "SENT"

# Email schedule
SCHEDULE_LIMIT = 60 * 2

# Excel file
FILE_BASE_PATH = f"{os.getcwd()}"
EXCEL_TIME_FORMAT = "%d %b %Y, %H:%M"
EXCEL_EXTENSION = "xlsx"
TO_MEGA_BYTES = 1024 * 1024
MAX_FILE_SIZE = 10  # 10 mbs

# Encryption software
ENCRYPT_SOFTWARE_DIR = "/home/nplaybook/msoffice/"