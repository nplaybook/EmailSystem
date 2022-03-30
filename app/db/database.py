import os

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app


BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with app.app_context():
    try:
        URI = f"{current_app.config['DB_DIALECT']}:///{BASE_DIR}/{current_app.config['DB_NAME']}"
    except:
        URI = f"""
        {current_app.config['DB_DIALECT']}://{current_app.config['DB_USER']}:{current_app.config['DB_PWD']}
        @{current_app.config['DB_HOST']}:{current_app.config['DB_PORT']}/{current_app.config['DB_NAME']}
        """

engine = create_engine(URI, echo=True)
Session = sessionmaker()