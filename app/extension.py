from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery import Celery


def init_engine(dialect: str, dir: str, name: str):
    """Create sqlalchemy engine

    :param dialect: type of database that will be initiated
    :param dir: db base directory
    :param name: db name
    :return: database engine object
    """

    URI: str = f"{dialect}:///{dir}/{name}"
    return create_engine(URI, echo=False)


def init_session():
    """Create sqlalchemy session"""

    return sessionmaker()


def init_celery(
    broker: str,
    backend: str,
    accept_content: str,
    result_serializer: str
) -> Celery:
    """Create celery worker

    :param broker: broker's ip address
    :param backend: database that will be used to store the result
    :param accept_content: data type that will be processed
    :param result_serializer: serialized data type
    :return: Celery object
    """

    celery = Celery("tasks", broker=broker, backend=backend)
    celery.conf.update(
        # task_serializer=CELERY_TASK_SERIALIZER,
        accept_content=accept_content,
        result_serializer=result_serializer
    )
    return celery
