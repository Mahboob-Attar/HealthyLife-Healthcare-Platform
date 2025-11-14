from flask import Blueprint, render_template, jsonify
import pymysql

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

DB_CONFIG = {
    "host": "localhost",
    "user": "Healthylife",
    "password": "Health@2025//",
    "database": "healthydb",     # ✅ FIXED (your actual DB)
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)


# -------------------------
# Dashboard Page
# -------------------------
@dashboard_bp.route("/")
def dashboard():
    return render_template("dashboard.html")


# -------------------------
# Dashboard Data API
# -------------------------
@dashboard_bp.route("/data")
def dashboard_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        data = {}

        # Total doctors
        cursor.execute("SELECT COUNT(*) AS total_doctors FROM doctors")
        data["total_doctors"] = cursor.fetchone()["total_doctors"]

        # Doctors by specialization
        cursor.execute("""
            SELECT specialization, COUNT(*) AS count 
            FROM doctors 
            GROUP BY specialization
        """)
        data["specializations"] = cursor.fetchall()

        # Total users (if table does not exist → return 0 gracefully)
        try:
            cursor.execute("SELECT COUNT(*) AS total_users FROM users")
            data["total_users"] = cursor.fetchone()["total_users"]
        except:
            data["total_users"] = 0

        # ML accuracy dummy data
        data["ml_accuracy"] = {
            "Disease A": 92,
            "Disease B": 87,
            "Disease C": 95
        }

        return jsonify({"success": True, "data": data})

    except Exception as e:
        print("Dashboard API Error:", e)
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
