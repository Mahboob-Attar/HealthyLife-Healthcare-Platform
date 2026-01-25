from flask import Blueprint, render_template, jsonify
from server.blueprints.services.admin.service import AdminService

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@admin_bp.route("/dashboard/data")
def dashboard_data():
    try:
        data = AdminService.get_dashboard_stats()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        print("❌ Dashboard Data Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500


@admin_bp.route("/dashboard/ratings")
def feedback_ratings_data():
    try:
        result = AdminService.get_feedback_ratings()
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        print("❌ Feedback Ratings Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500


@admin_bp.route("/dashboard/reviews")
def admin_reviews():
    try:
        feedbacks = AdminService.get_all_feedback()
        return render_template("admin_reviews.html", feedbacks=feedbacks)
    except Exception as e:
        print("❌ Admin Reviews Error:", e)
        return "Database connection error"
