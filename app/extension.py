from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery import Celery

from app.config import (
    DB_BASE_DIR, DB_DIALECT, DB_NAME,
    CELERY_BROKER_URL, CELERY_RESULT_BACKEND,
    CELERY_ACCEPT_CONTENT, CELERY_RESULT_SERIALIZER
    # CELERY_TASK_SERIALIZER
)


def init_engine():
    """Create sqlalchemy engine"""

    URI: str = f"{DB_DIALECT}:///{DB_BASE_DIR}/{DB_NAME}"
    return create_engine(URI, echo=False)


def init_session():
    """Create sqlalchemy session"""

    return sessionmaker()


def init_celery():
    """Create celery worker"""

    celery = Celery(
        "tasks",
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND
        )
    celery.conf.update(
        # task_serializer=CELERY_TASK_SERIALIZER,
        accept_content=CELERY_ACCEPT_CONTENT,
        result_serializer=CELERY_RESULT_SERIALIZER
    )
    return celery
