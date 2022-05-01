import json

import socket
from flask import g, request, Response, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.schemas import EmailDirectlyPayload
from app.blueprint.email.utils import EmailUtils
from app.library.typing import JSON
from app.library.creds import CredUtils
from app.library.response import SuccessResponse, ErrorResponse


email_bp = Blueprint("email", __name__, url_prefix="/email")


@email_bp.post(rule="/direct")
def send_directly() -> JSON:
    """Send email right away"""

    # validate payload
    try:
        payload = EmailDirectlyPayload(**request.json)
    except ValidationError as err:
        return Response(
            json.dumps(
                ErrorResponse(message="Input data error", error=err.errors()).
                    generate_response()
                ), 400
        )
    else:
        payload = payload.dict()
        payload["smtp"]["password"] = CredUtils().decode(payload["smtp"]["password"])
        payload["email"]["schedule_at"] = None

    # insert email details operation
    e = EmailUtils(payload)
    try:
        e.insert_email_record(db=g.session)
        e.insert_recipient_record(db=g.session)
    except SQLAlchemyError as err:
        g.session.rollback()
        err = err.args[0]
        return Response(
            json.dumps(
                ErrorResponse(message="Database error", error=err).
                    generate_response()
                ), 500
        )

    # send email operation
    try:
        e.send_email(db=g.session)
    except socket.error as err:
        return Response(
            json.dumps(
                ErrorResponse(message="Couldn't connect to email provider", error=str(err)).
                    generate_response()
                ), 503
        )

    return Response(
        json.dumps(
            SuccessResponse(message="Email sent").
                generate_response()
        ), 200
    )
