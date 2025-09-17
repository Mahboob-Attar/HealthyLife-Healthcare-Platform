from flask import Blueprint, request, jsonify
import pymysql, os
from datetime import datetime
from werkzeug.utils import secure_filename

doctor_bp = Blueprint("doctor_bp", __name__)

# ================= DB CONFIG =================
DB_CONFIG = {
    "host": "localhost",
    "user": "Healthylife",      
    "password": "Health@2025//",   
    "database": "healthylifedb",
    "charset": "utf8mb4"
}

# ================= UPLOADS =================
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads", "doctors")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= DB CONNECTION =================
def get_connection():
    return pymysql.connect(**DB_CONFIG)

# ================= ROUTES =================
@doctor_bp.route("/register_doctor", methods=["POST"])
def register_doctor():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Extract form fields
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        experience = request.form.get("experience")
        specialization = request.form.get("specialization")
        services = request.form.get("services")
        clinic = request.form.get("clinic")
        location = request.form.get("location")
        photo = request.files.get("photo")

        # Check required fields
        if not (name and phone and email and specialization and photo):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Check duplicate email
        cursor.execute("SELECT id FROM doctors WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"}), 409

        # Save photo file
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOAD_FOLDER, filename)
        photo.save(photo_path)

        # Insert doctor
        sql = """
        INSERT INTO doctors 
        (name, phone, email, experience, specialization, services, clinic, location, photo_path, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            name, phone, email, int(experience), specialization,
            services, clinic, location, photo_path, datetime.utcnow()
        )
        cursor.execute(sql, values)
        conn.commit()

        return jsonify({"success": True})

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "Server error. Please contact support."}), 500

    finally:
        cursor.close()
        conn.close()
