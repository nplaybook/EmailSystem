import json
from lib2to3.pytree import Base
from typing import Dict, Any

from flask import request, redirect, url_for
from flask import Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import app
from app.config.config import PAYLOAD_EMAIL, STATUS_PENDING, PAYLOAD_RECIPIENT
from app.db import Session, engine
from app.models import Event, Email, Recipient
from app.schemas.email import SaveEmailPayload
from app.utils.orm_serialize import serialize_many
from app.utils.response import success_response, error_response


@app.get("/event")
def get_events():
    try:
        with Session(bind=engine) as session:
            events = session.query(Event).all()
        events = serialize_many(events)
    except BaseException as err:
        return Response(
            json.dumps(error_response(message="Process error", err=err.errors())), 400
            )
    return Response(
            json.dumps(success_response(message="Request success", data=events)), 200
            )


@app.post("/save_emails")
def save_emails() -> Dict[str, Any]:
    payload = request.json

    # validate payload using pydantic
    try:
        payload = SaveEmailPayload(**payload)
    except ValidationError as err:
        return Response(
            json.dumps(error_response(message="Validation error", err=err.errors())), 400
            )
    else:
        payload = payload.dict()
    
    # insert email
    email_data: dict = {key: payload[key] for key in json.loads(PAYLOAD_EMAIL)}
    email_data["status"] = STATUS_PENDING
    with Session(bind=engine) as session:
        try:
            new_email = Email(**email_data)  
            session.add(new_email)
            session.commit()
            session.flush()
        except SQLAlchemyError as err:
            session.rollback()
            return Response(
                json.dumps(error_response(message="Database error", err=err.args)), 500
            )
        else:
            email_id = new_email.id

    # insert recipient
    to_email = payload[PAYLOAD_RECIPIENT]
    recipient_data: list = [{"email_id": email_id, "to_email": email} for email in to_email]
    with Session(bind=engine) as session:
        try:
            new_recipient = [Recipient(**recipient) for recipient in recipient_data]
            session.add_all(new_recipient)
            session.commit()
        except SQLAlchemyError as err:
            session.rollback()
            return Response(
                json.dumps(error_response(message="Database error", err=err.args)), 500
            )

    return Response(
        json.dumps(success_response(message="Request success")), 201
    )