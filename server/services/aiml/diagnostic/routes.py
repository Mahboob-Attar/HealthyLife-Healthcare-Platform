from flask import Blueprint, render_template, request, jsonify
from services.aiml.diagnostic.service import DiagnosticService

diagnostic_bp = Blueprint("diagnostic_bp", __name__, url_prefix="/diagnostic")

@diagnostic_bp.route("/", methods=["GET"])
def page():
    return render_template("diagnostic.html")


@diagnostic_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        result = DiagnosticService.predict(data)
        return jsonify(result), 200

    except Exception as e:
        print("❌ Diagnostic Prediction Error:", e)
        return jsonify({"status": "error", "message": "Server Error"}), 500
