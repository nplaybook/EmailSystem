import os

from app.utils.commons import open_file


class Config:
    config_path = f'{os.getcwd()}/config.yaml'
    config_content = open_file(path=config_path)

    SECRET_KEY = config_content["SECRET_KEY"]

    DB_DIALECT = config_content["DB"]["DIALECT"]
    DB_USER = config_content["DB"]["USERNAME"]
    DB_PWD = config_content["DB"]["PASSWORD"]
    DB_HOST = config_content["DB"]["HOST"]
    DB_PORT = config_content["DB"]["PORT"]
    DB_NAME = config_content["DB"]["NAME"]

    EMAIL_KEYS = config_content["PAYLOAD"]["EMAIL"]
    RECIPIENT_KEYS  = config_content["PAYLOAD"]["RECIPIENT"]

    INSERT_EMAIL_STATUS = config_content["CONST"]["EMAIL"]["INSERT_STATUS"]