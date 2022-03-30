from typing import Dict, List, Any

from app.models.base import Base as ModelBase


def serialize(obj: ModelBase) -> Dict[str, Any]:
    """Map ORM/SQLAlchemy object to dictionary
    
    :param obj: orm model
    :return: mapped orm in dictionary 
    """
    
    keys = [column.key for column in obj.__table__.columns]
    return {key: getattr(obj, key) for key in keys}


def serialize_many(objs: List[ModelBase]) -> List[Dict[str, Any]]:
    """Map list of ORM/SQLAlchemy object to list of dictionary

    :param objs: list of orm model
    :return: list of mapped orm model in dictionary
    """
    
    return [serialize(obj) for obj in objs]