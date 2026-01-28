from flask import Blueprint, render_template, jsonify, session, redirect
from server.blueprints.services.admin.service import AdminService

admin = Blueprint("admin_bp", __name__, url_prefix="/admin")

# ---------------- AUTH GUARD ----------------
def admin_required():
    return session.get("logged_in") and session.get("role") == "admin"


# ---------------- DASHBOARD PAGE ----------------
@admin.route("/dashboard")
def dashboard_page():
    if not admin_required():
        return redirect("/")
    return render_template("dashboard.html")


# ---------------- DASHBOARD DATA (AJAX) ----------------
@admin.route("/dashboard/data")
def dashboard_data():
    if not admin_required():
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    try:
        data = AdminService.get_dashboard_stats()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        print("❌ Dashboard Data Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500


# ---------------- FEEDBACK RATINGS DATA ----------------
@admin.route("/dashboard/ratings")
def feedback_ratings_data():
    if not admin_required():
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    try:
        result = AdminService.get_feedback_ratings()
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        print("❌ Feedback Ratings Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500


# ---------------- ADMIN REVIEWS PAGE ----------------
@admin.route("/dashboard/reviews")
def admin_reviews():
    if not admin_required():
        return redirect("/")

    try:
        feedbacks = AdminService.get_all_feedback()
        return render_template("admin_reviews.html", feedbacks=feedbacks)
    except Exception as e:
        print("❌ Admin Reviews Error:", e)
        return "Database connection error"


# # ---------------- LOGOUT ----------------
@admin.route("/logout", methods=["POST"])
def admin_logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out"}), 200
