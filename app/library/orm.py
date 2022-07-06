from typing import List, NoReturn

from app.models.base import Base as ModelBase
from app.library.typing import JSON, JSON_ARRAY


class OrmUtils:

    def __init__():
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

    @staticmethod
    def get_columns_name(objs: List[ModelBase], many: bool) -> List[str]:
        """Get query's column name. Can be done by accessing one of the
        item in result's list
        
        :param objs: list of orm model
        :param many: True if it contains multiple columns
        :return: list of column names
        """

        if many:
            return [column.key for column in objs[0].__table__.columns]
        return list(objs[0].keys())
