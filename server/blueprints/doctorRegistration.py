from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime

doctor_bp = Blueprint("doctor_bp", __name__)

# MySQL configuration (adjust to your database)
DB_CONFIG = {
    "host": "localhost",
    "user": "your_username",
    "password": "your_password",
    "database": "healthydb",
    "charset": "utf8mb4"
}

# Doctor registration route
@doctor_bp.route("/register_doctor", methods=["POST"])
def register_doctor():
    data = request.get_json()
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # Check if email exists
        cursor.execute("SELECT id FROM doctors WHERE email=%s", (data["email"],))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already registered."})

        # Insert doctor
        sql = """
        INSERT INTO doctors 
        (name, phone, email, experience, specialization, services, clinic, location, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        values = (
            data["name"],
            data["phone"],
            data["email"],
            int(data["experience"]),
            data["specialization"],
            data.get("services"),
            data.get("clinic"),
            data.get("location"),
            datetime.utcnow()
        )

        cursor.execute(sql, values)
        conn.commit()
        return jsonify({"success": True})

    except Exception as e:
        print("Error:", e)
        return jsonify({"success": False, "message": "Server error. Please contact support."})

    finally:
        cursor.close()
        conn.close()

# Function to create table if it doesn't exist
def create_table():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        experience INT NOT NULL,
        specialization VARCHAR(100) NOT NULL,
        services TEXT,
        clinic VARCHAR(100),
        location VARCHAR(100),
        created_at DATETIME
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
