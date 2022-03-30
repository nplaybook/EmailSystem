import json
from lib2to3.pytree import convert

from flask import jsonify, request, abort, current_app
from flask import Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import app
from app.db import Session, engine
from app.models import Event, Email, Recipient
from app.schemas.email import SaveEmailPayload
from app.utils.orm_serialize import serialize_many
from app.utils.response import success_response, error_response
from app.utils.commons import convert_to_strftime


@app.get("/")
def index():
    return "Hello world"


@app.get("/event")
def get_events():
    with Session(bind=engine) as session:
        events = session.query(Event).all()
    events = serialize_many(events)
    return Response(
        json.dumps(success_response(message="Request success", data=events)), 200
        )


@app.post("/save_emails")
def save_emails():
    payload = request.json

    # change input datetime to timestamp format

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
    email_data: dict = {key: payload[key] for key in current_app.config["EMAIL_KEYS"]}
    email_data["status"] = current_app.config["INSERT_EMAIL_STATUS"]
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
    to_email = payload[current_app.config["RECIPIENT_KEYS"]]
    recipient_data: list = [{"email_id": email_id, "to_email": email} for email in to_email]
    with Session(bind=engine) as session:
        try:
            new_recipient = [Recipient(**recipient) for recipient in recipient_data]
            session.add_all(new_recipient)
            session.commit()
            session.flush()
        except SQLAlchemyError as err:
            session.rollback()
            return Response(
                json.dumps(error_response(message="Database error", err=err.args)), 500
            )

    # add to queue / schedule email program


    return Response(
        json.dumps(success_response(message="Request success")), 200
    )