from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from db import get_connection  # <- Reuse pooled connection

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def dashboard():
    return render_template("dashboard.html")


@dashboard_bp.route("/data")
def dashboard_data():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        data = {}

        cursor.execute("SELECT COUNT(*) AS total_doctors FROM doctors")
        data["total_doctors"] = cursor.fetchone()["total_doctors"]

        cursor.execute("SELECT specialization, COUNT(*) AS count FROM doctors GROUP BY specialization")
        data["specializations"] = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@dashboard_bp.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    username = data.get("username")
    rating = data.get("rating")
    review = data.get("review")

    if not username or not rating or not review:
        return jsonify({"success": False, "message": "Invalid data"})

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (username, rating, review, created_at) VALUES (%s, %s, %s, %s)",
            (username, rating, review, datetime.now())
        )
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"success": True})

    except Exception as e:
        print("Submit Feedback Error:", e)
        return jsonify({"success": False, "message": "Database error"})


@dashboard_bp.route("/feedback_ratings")
def feedback_ratings_data():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        feedback_ratings = {str(i): 0 for i in range(1, 6)}
        cursor.execute("SELECT rating, COUNT(*) AS count FROM feedback GROUP BY rating")
        rows = cursor.fetchall()

        for row in rows:
            feedback_ratings[str(row['rating'])] = row['count']

        cursor.close()
        conn.close()
        return jsonify({"success": True, "data": {"feedback_ratings": feedback_ratings}})

    except Exception as e:
        print("Feedback Ratings API Error:", e)
        return jsonify({"success": False, "message": str(e)})


@dashboard_bp.route("/admin_reviews")
def admin_reviews():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedback ORDER BY created_at DESC")
        feedbacks = cursor.fetchall()

        cursor.close()
        conn.close()
        return render_template("admin_reviews.html", feedbacks=feedbacks)

    except Exception as e:
        print("Admin Reviews Error:", e)
        return "Database connection error"
