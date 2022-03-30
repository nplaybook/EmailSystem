from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

from .routes import routes
from app.utils.mailing import check_scheduled_email