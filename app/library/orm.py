from typing import List, NoReturn

from app.models.base import Base as ModelBase
from app.library.typing import JSON, JSON_ARRAY


class OrmUtils:

    def __init__() -> NoReturn:
        pass

    @staticmethod
    def serialize(obj: ModelBase) -> JSON:
        """Map ORM/SQLAlchemy object to dictionary

        :param obj: orm model
        :return: mapped orm in dictionary
        """

        keys = [column.key for column in obj.__table__.columns]
        return {key: getattr(obj, key) for key in keys}

    @staticmethod
    def serialize_many(objs: List[ModelBase]) -> JSON_ARRAY:
        """Map list of ORM/SQLAlchemy object to list of dictionary

        :param objs: list of orm model
        :return: list of mapped orm model in dictionary
        """

        return [OrmUtils.serialize(obj) for obj in objs]
