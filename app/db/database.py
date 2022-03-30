import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app


load_dotenv(".env")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with app.app_context():
    try:
        URI = f"{os.environ['DB_DIALECT']}:///{BASE_DIR}/{os.environ['DB_NAME']}"
    except:
        URI = f"""
        {os.environ['DB_DIALECT']}://{os.environ['DB_USER']}:{os.environ['DB_PWD']}
        @{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}
        """

engine = create_engine(URI, echo=True)
Session = sessionmaker()