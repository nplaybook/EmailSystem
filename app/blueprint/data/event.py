import json

from flask import g, Response
from sqlalchemy.exc import SQLAlchemyError

from app.models import Event
from app.library.orm import OrmUtils
from app.library.response import SuccessResponse, ErrorResponse


def get_event():
    """Get all event data"""

    try:
        providers = g.session.query(Event).all()
    except SQLAlchemyError as err:
        return Response(
            json.dumps(
                ErrorResponse(message="Database error", error=err.args[0]).
                    generate_response()
                ), 500
        )

    providers = OrmUtils.serialize_many(providers)
    return Response(
        json.dumps(
            SuccessResponse(message="Request succeess", data=providers).
                generate_response()
        ), 200
    )