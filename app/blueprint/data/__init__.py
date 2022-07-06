from flask import Blueprint

from app.blueprint.data.provider import get_provider
from app.blueprint.data.event import get_event


data_bp = Blueprint("data", __name__, url_prefix="/data")
data_bp.add_url_rule("/provider", view_func=get_provider, methods=["GET"])
data_bp.add_url_rule("/event", view_func=get_event, methods=["GET"])
