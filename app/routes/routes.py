import os
import json
from dotenv import load_dotenv

from flask import request, redirect, url_for
from flask import Response
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app import app
from app.db import Session, engine
from app.models import Event, Email, Recipient
from app.schemas.email import SaveEmailPayload
from app.utils.orm_serialize import serialize_many
from app.utils.response import success_response, error_response

load_dotenv("./env")


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
    email_data: dict = {key: payload[key] for key in json.loads(os.environ["PAYLOAD_EMAIL"])}
    email_data["status"] = os.environ["EMAIL_INSERT_STATUS"]
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
    to_email = payload[os.environ["PAYLOAD_RECIPIENT"]]
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

    # check if need to send now
    if payload["is_send_now"]:
        redirect(url_for("send_email"), message=email_id)

    # add to queue / schedule email program


    return Response(
        json.dumps(success_response(message="Request success")), 200
    )


@app.post("/send_email")
def send_email():
    pass