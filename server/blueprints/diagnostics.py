from flask import Blueprint, render_template, request, jsonify

diagnostics_bp = Blueprint("diagnostics", __name__, url_prefix="/diagnostics")

@diagnostics_bp.route("/")
def diagnostics():
    return render_template("diagnostics.html")

@diagnostics_bp.route("/predict", methods=["POST"])
def predict():
    """
    API Endpoint for Disease Prediction
    Expects: JSON => { "symptoms": "fever, cough" }
    Returns: JSON => { "prediction": "Flu" }
    """
    try:
        data = request.get_json(force=True)
        symptoms = data.get("symptoms", "").strip()

        # Dummy Prediction Logic (replace with ML model later)
        if "fever" in symptoms.lower() or "cough" in symptoms.lower():
            prediction = "Flu"
        elif "headache" in symptoms.lower():
            prediction = "Migraine"
        else:
            prediction = "Unknown Disease"

        return jsonify({
            "status": "success",
            "prediction": prediction
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
