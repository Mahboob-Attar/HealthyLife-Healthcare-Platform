from flask import Blueprint, render_template, session, jsonify
from server.blueprints.services.admin.service import AdminService
from server.config.db import get_connection

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


def login_required():
    return session.get("logged_in") is True


@dashboard.route("/")
def dashboard_page():
    if not login_required():
        return render_template("unauthorized.html"), 403
    
    return render_template(
        "dashboard.html",
        is_admin=session.get("is_admin", False)
    )


@dashboard.route("/data")
def dashboard_data():
    if not login_required():
        return jsonify({"success": False}), 403

    role = session.get("role")

    # Common data for both admin and user
    stats = AdminService.get_dashboard_stats()
    ratings = AdminService.get_feedback_ratings()

    response_data = {
        "stats": stats,
        "ratings": ratings
    }

    # Admin-only extra data
    if role == "admin":
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, name, email, created_at FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()

        response_data["users"] = users

    return jsonify({
        "success": True,
        "role": role,
        "data": response_data
    })
