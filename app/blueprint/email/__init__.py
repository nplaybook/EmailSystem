from flask import Blueprint

# from app.blueprint.email.email import send_directly, send_later
from app.blueprint.email.email import send_directly
from app.blueprint.email.export_report import send_export_data


email_bp = Blueprint("email", __name__, url_prefix="/email")
email_bp.add_url_rule("/direct", view_func=send_directly, methods=["POST"])
# email_bp.add_url_rule("/scheduled", view_func=send_later, methods=["POST"])
email_bp.add_url_rule("/report", view_func=send_export_data, methods=["POST"])