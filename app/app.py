from flask import Flask, g

from app.extension import (
    init_engine, init_session
    # init_celery
)


def make_app(config: str) -> Flask:
    """Main caller to create Flask appication

    :param config: path where configuration file resides
    :return app: Flask application
    """

    app = Flask(__name__)
    app.config.from_pyfile(config)

    # celery = init_celery()

    # register blueprint
    from app.blueprint.data import data_bp
    from app.blueprint.email import email_bp

    app.register_blueprint(data_bp)
    app.register_blueprint(email_bp)

    return app


app = make_app("config.py")

# application context
@app.before_request
def get_db_con():
    if "session" not in g:
        db_engine = init_engine()
        db_session = init_session()
        g.session = db_session(bind=db_engine)


@app.after_request
def close_db_con(response):
    session = g.pop("session", None)
    if session is not None:
        session.close()
    return response
