from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from db import get_connection   # <— use shared pool

feedback_bp = Blueprint("feedback_bp", __name__)


# ---- Submit Feedback ----
@feedback_bp.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    username = data.get("username")
    rating = data.get("rating")
    review = data.get("review")

    if not username or not rating or not review:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO feedback (username, rating, review, created_at) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, rating, review, datetime.now()))
        conn.commit()

        return jsonify({"success": True})

    except Exception as e:
        print("Submit Feedback Error:", e)
        return jsonify({"success": False, "message": "Database error"}), 500

    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ---- Admin View Feedback ----
@feedback_bp.route("/admin_reviews")
def admin_reviews():
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        feedbacks = cursor.fetchall()

        return render_template("admin_reviews.html", feedbacks=feedbacks)

    except Exception as e:
        print("Admin Reviews Error:", e)
        return "Database connection error"

    finally:
        if cursor: cursor.close()
        if conn: conn.close()
