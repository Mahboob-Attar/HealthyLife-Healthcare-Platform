from flask import Blueprint, render_template, jsonify
import pymysql

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

DB_CONFIG = {
    "host": "localhost",
    "user": "Healthylife",
    "password": "Health@2025//",
    "database": "healthylifedb",
    "charset": "utf8mb4"
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

@dashboard_bp.route("/")
def dashboard():
    return render_template("dashboard.html")

@dashboard_bp.route("/dashboard_data")
def dashboard_data():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    data = {}
    try:
        # Total doctors
        cursor.execute("SELECT COUNT(*) AS total_doctors FROM doctors")
        data["total_doctors"] = cursor.fetchone()["total_doctors"]

        # Doctors by specialization
        cursor.execute("SELECT specialization, COUNT(*) as count FROM doctors GROUP BY specialization")
        data["specializations"] = cursor.fetchall()

        # Total users
        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        data["total_users"] = cursor.fetchone()["total_users"]

        # ML model accuracy (for demo, static value; can replace with actual model info)
        data["ml_accuracy"] = {
            "Disease A": 92,
            "Disease B": 87,
            "Disease C": 95
        }

        return jsonify({"success": True, "data": data})
    except Exception as e:
        print("Dashboard error:", e)
        return jsonify({"success": False, "message": "Server error"}), 500
    finally:
        cursor.close()
        conn.close()
