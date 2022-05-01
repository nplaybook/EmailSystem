import json

from flask import g, Response, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.models import Provider, Event
from app.library.orm import OrmUtils
from app.library.response import SuccessResponse, ErrorResponse


data_bp = Blueprint("data", __name__, url_prefix='/data')


@data_bp.get(rule="/provider")
def get_provider():
    """Get all provider data"""

    try:
        providers = g.session.query(Provider).all()
    except SQLAlchemyError as err:
        return Response(
            json.dumps(
                ErrorResponse(message="Database error", error=err.args[0]).
                    generate_response()
                ), 500
        )

    providers = OrmUtils().serialize_many(providers)
    return Response(
        json.dumps(
            SuccessResponse(message="Request succeess", data=providers).
                generate_response()
        ), 200
    )


@data_bp.get(rule="/event")
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

    providers = OrmUtils().serialize_many(providers)
    return Response(
        json.dumps(
            SuccessResponse(message="Request succeess", data=providers).
                generate_response()
        ), 200
    )
