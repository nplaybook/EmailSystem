import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from app.config.config import (
    DB_DIALECT, DB_NAME, DB_USERNAME, DB_PASSWORD,
    DB_HOST, DB_PORT, DB_NAME
)


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with app.app_context():
    try:
        URI = f"{DB_DIALECT}:///{BASE_DIR}/{DB_NAME}"
    except:
        URI = f"""
        {DB_DIALECT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}
        """

engine = create_engine(URI, echo=True)
Session = sessionmaker()