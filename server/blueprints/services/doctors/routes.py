from flask import Blueprint, request, jsonify, send_from_directory
from server.blueprints.services.doctors.service import DoctorService


doctors = Blueprint("doctors_bp", __name__, url_prefix="/doctors")


# ---------------------------------------------------------
# Serve doctor profile images
# URL Example: /doctors/image/somefile.jpg
# ---------------------------------------------------------
@doctors.route("/image/<filename>")
def doctor_image(filename):
    try:
        file_path = DoctorService.get_image_path()
        return send_from_directory(file_path, filename)
    except Exception as e:
        print("❌ Image Serve Error:", e)
        return "Image not found", 404


# ---------------------------------------------------------
# Register Doctor (POST)
# URL: /doctors/register
# ---------------------------------------------------------
@doctors.route("/register", methods=["POST"])
def register_doctor():
    try:
        response = DoctorService.register(request)  # returns dict with 'status'
        return jsonify({
            "success": response.get("success"),
            "message": response.get("message")
        }), response.get("status", 500)
    except Exception as e:
        print("❌ Register Doctor Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500


# ---------------------------------------------------------
# Get All Doctors (GET)
# URL: /doctors/all
# ---------------------------------------------------------
@doctors.route("/all", methods=["GET"])
def get_doctors():
    try:
        doctors = DoctorService.get_all()
        return jsonify({"success": True, "doctors": doctors}), 200
    except Exception as e:
        print("❌ Get Doctors Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500


# ---------------------------------------------------------
# OPTIONAL: Check Email Exists (GET)
# URL: /doctors/check-email?email=...
# ---------------------------------------------------------
@doctors.route("/check-email", methods=["GET"])
def check_email():
    try:
        email = request.args.get("email")
        exists = DoctorService.check_email_exists(email)
        return jsonify({"exists": exists}), 200
    except Exception as e:
        print("❌ Check Email Error:", e)
        return jsonify({"exists": False}), 500


# ---------------------------------------------------------
# OPTIONAL: Check Phone Exists (GET)
# URL: /doctors/check-phone?phone=...
# ---------------------------------------------------------
@doctors.route("/check-phone", methods=["GET"])
def check_phone():
    try:
        phone = request.args.get("phone")
        exists = DoctorService.check_phone_exists(phone)
        return jsonify({"exists": exists}), 200
    except Exception as e:
        print("❌ Check Phone Error:", e)
        return jsonify({"exists": False}), 500
