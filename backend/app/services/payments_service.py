from flask import request, jsonify
from config import DevelopmentConfig as Config
import requests
def capture_payment_service():
    """ Capture PayPal payment """
    try:
        data = request.json
        order_id = data.get("orderID")
        
        if not order_id:
            return jsonify({"error": "No order ID provided"}), 400

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_paypal_access_token()}"
        }
        response = requests.post(
            f"{Config.PAYPAL_API}/v2/checkout/orders/{order_id}/capture",
            headers=headers
        )
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_paypal_access_token():
    """ Get an access token from PayPal """
    auth = (Config.PAYPAL_CLIENT_ID, Config.PAYPAL_SECRET)
    response = requests.post(
        f"{Config.PAYPAL_API}/v1/oauth2/token",
        auth=auth,
        data={"grant_type": "client_credentials"}
    )
    return response.json().get("access_token")