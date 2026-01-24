import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from db import get_connection  # <— using shared connection pool

load_dotenv()

doctor_bp = Blueprint("doctor_bp", __name__)

# ---- Upload Settings ----
UPLOAD_FOLDER = os.getenv("UPLOAD_PATH", "uploads/doctors")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

# Serve doctor images
@doctor_bp.route('/doctor_image/<filename>')
def doctor_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---- Register Doctor ----
@doctor_bp.route("/register_doctor", methods=["POST"])
def register_doctor():
    conn = None
    cursor = None

    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        experience = request.form.get("experience")
        specialization = request.form.get("specialization")
        services = request.form.get("services")
        clinic = request.form.get("clinic")
        location = request.form.get("location")
        photo = request.files.get("photo")

        # Validate required fields
        if not all([name, phone, email, specialization, photo]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if not allowed_file(photo.filename):
            return jsonify({"success": False, "message": "Invalid file type"}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Duplicate email check
        cursor.execute("SELECT id FROM doctors WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"}), 409

        # Save image
        ext = photo.filename.rsplit(".", 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        filename = secure_filename(unique_name)
        photo.save(os.path.join(UPLOAD_FOLDER, filename))

        # Insert record
        sql = """
            INSERT INTO doctors
            (name, phone, email, experience, specialization, services, clinic, location, photo_path, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            name, phone, email, experience, specialization, services,
            clinic, location, filename, datetime.utcnow()
        ))

        conn.commit()
        return jsonify({"success": True, "message": "Doctor registered successfully."})

    except Exception as e:
        print("❌ register_doctor Error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ---- Get All Doctors ----
@doctor_bp.route("/get_doctors", methods=["GET"])
def get_doctors():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, name, specialization, photo_path, clinic, location
            FROM doctors ORDER BY created_at DESC
        """)

        doctors = cursor.fetchall()

        # Assign default images
        for doc in doctors:
            doc["photo_path"] = doc.get("photo_path") or "default.jpg"

        return jsonify({"success": True, "doctors": doctors})

    except Exception as e:
        print("❌ get_doctors Error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
