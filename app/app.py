from flask import Flask, g, current_app

from app.extension import (
    init_engine, init_session, init_celery
)


def make_app(config: str) -> Flask:
    """Main caller to create Flask appication

    :param config: path where configuration file resides
    :return app: Flask application
    """

    app = Flask(__name__)
    app.config.from_pyfile(config)

    # register blueprint
    from app.blueprint.data import data_bp
    from app.blueprint.email import email_bp

    app.register_blueprint(data_bp)
    app.register_blueprint(email_bp)

    return app


app = make_app("config.py")
# celery = init_celery(
#     broker=current_app.config["CELERY_BROKER_URL"],
#     backend=current_app.config["CELERY_RESULT_BACKEND"],
#     accept_content=current_app.config["CELERY_ACCEPT_CONTENT"],
#     result_serializer=current_app.config["CELERY_RESULT_SERIALIZER"]
# )

# application context
@app.before_request
def get_db_con():
    if "session" not in g:
        db_engine = init_engine(
            dialect=current_app.config["DB_DIALECT"],
            dir=current_app.config["DB_BASE_DIR"],
            name=current_app.config["DB_NAME"]
        )
        db_session = init_session()
        g.session = db_session(bind=db_engine)


@app.after_request
def close_db_con(response):
    session = g.pop("session", None)
    if session is not None:
        session.close()
    return response
