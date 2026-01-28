from flask import Blueprint, request, jsonify
from .otp_service import create_and_send_otp, verify_otp as verify_otp_service
from .service import auth_signup, auth_login, reset_password

auth = Blueprint("auth_bp", __name__, url_prefix="/auth")

# SEND OTP
@auth.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data.get("email")
    purpose = data.get("purpose", "signup")

    if not email:
        return jsonify({"status": "error", "msg": "Email required"}), 400

    result = create_and_send_otp(email, purpose)
    return jsonify(result), 200


# VERIFY OTP
@auth.route("/verify-otp", methods=["POST"])
def verify_otp_route():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    purpose = data.get("purpose", "signup")

    if not email or not otp:
        return jsonify({"status": "error", "msg": "Email and OTP required"}), 400

    result = verify_otp_service(email, otp, purpose)
    return jsonify(result), 200


# SIGNUP (USER ONLY)
@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    return auth_signup(data)



# LOGIN (USER / ADMIN)
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return auth_login(data)



# RESET PASSWORD
@auth.route("/reset", methods=["POST"])
def reset():
    data = request.get_json()
    return reset_password(data)
