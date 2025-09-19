from flask import Blueprint, request, jsonify, send_from_directory
import pymysql, os
from datetime import datetime
from werkzeug.utils import secure_filename

doctor_bp = Blueprint("doctor_bp", __name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "Healthylife",
    "password": "Health@2025//",
    "database": "healthylifedb",
    "charset": "utf8mb4"
}

# Upload folder: server/doctors_upload_images
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "doctors_upload_images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_connection():
    return pymysql.connect(**DB_CONFIG)

# Serving uploaded images via Flask route
@doctor_bp.route('/doctor_image/<filename>')
def doctor_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@doctor_bp.route("/register_doctor", methods=["POST"])
def register_doctor():
    conn = get_connection()
    cursor = conn.cursor()
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

        if not all([name, phone, email, specialization, photo]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        if not allowed_file(photo.filename):
            return jsonify({"success": False, "message": "Invalid file type"}), 400

        cursor.execute("SELECT id FROM doctors WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered"}), 409

        filename = secure_filename(photo.filename)
        photo.save(os.path.join(UPLOAD_FOLDER, filename))
        photo_db_path = filename  # save only the filename

        sql = """
        INSERT INTO doctors
        (name, phone, email, experience, specialization, services, clinic, location, photo_path, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, phone, email, int(experience), specialization,
                  services, clinic, location, photo_db_path, datetime.utcnow())
        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"success": True, "message": "Doctor registered successfully."})

    except Exception as e:
        print("Error in register_doctor:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        cursor.close()
        conn.close()

@doctor_bp.route("/get_doctors", methods=["GET"])
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("SELECT id, name, specialization, photo_path, clinic, location FROM doctors ORDER BY created_at DESC")
        doctors = cursor.fetchall()
        for doc in doctors:
            if not doc.get("photo_path"):
                doc["photo_path"] = "default.jpg"  # fallback image; put default.jpg in doctors_upload_images
        return jsonify({"success": True, "doctors": doctors})
    except Exception as e:
        print("Error in get_doctors:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        cursor.close()
        conn.close()
