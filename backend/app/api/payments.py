from flask import Blueprint
from app.services.payments_service import capture_payment_service
payments_bp = Blueprint('payments', __name__)

@payments_bp.route("/paypal/capture", methods=["POST"])
def capture_payment():
    return capture_payment_service()