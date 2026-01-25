from flask import Blueprint, request, jsonify
from server.blueprints.services.feedback.service import FeedbackService

feedback_bp = Blueprint("feedback_bp", __name__, url_prefix="/feedback")

@feedback_bp.route("/submit", methods=["POST"])
def submit_feedback():
    try:
        data = request.json
        result = FeedbackService.store(data)
        return jsonify({"success": True, "message": "Feedback stored"}), 200
    except Exception as e:
        print("❌ Feedback Error:", e)
        return jsonify({"success": False, "message": "Server Error"}), 500
