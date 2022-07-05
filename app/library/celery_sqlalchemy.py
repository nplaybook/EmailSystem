from celery import Task
from flask import g


class SQLAlchemyTask(Task):
    """An abstract celery Task that ensures the connection to the
    database is closed on the task completion.
    """

    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        session = g.pop("session", None)
        if session is not None:
            session.close()
