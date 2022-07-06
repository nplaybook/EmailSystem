import json

from flask import g, request, Response
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.schemas import EmailDirectlyPayload, EmailLaterPayload
from app.library.typing import JSON
from app.library.creds import CredUtils
from app.library.backend_scripts import DBEmailTransaction
from app.library.response import SuccessResponse, ErrorResponse
from app.blueprint.email.utils import EmailPrep, send_email_task


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
        payload["smtp"]["password"] = CredUtils.decode(payload["smtp"]["password"])
        payload["email"]["schedule_at"] = None

    # insert email and recipient record
    email_prep = EmailPrep(payload["email"])
    email_record = email_prep.assign_pending_status()
    trx = DBEmailTransaction()
    try:
        trx.insert_email_record(db=g.session, email=email_record)
        recipient_record = email_prep.format_recipient_data(trx.email_id)
        trx.insert_recipient_record(db=g.session, recipients=recipient_record)
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
    # send_email_task.apply_async(kwargs={"db": g.session})
    send_email_task(db=g.session, payload=payload)
    # TODO: update email status
    return Response(
        json.dumps(
            SuccessResponse(message="Email sent").
                generate_response()
        ), 200
    )
