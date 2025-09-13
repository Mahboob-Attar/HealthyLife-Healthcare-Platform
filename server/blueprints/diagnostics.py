from flask import Blueprint, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle

# ============================================================
# Load datasets (make sure paths are correct inside your project)
# ============================================================
sym_des = pd.read_csv("datasets/symptoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv("datasets/medications.csv")
diets = pd.read_csv("datasets/diets.csv")

# ============================================================
# Load trained ML model
# ============================================================
with open("server/ml-models/svc.pkl", "rb") as f:
    svc = pickle.load(f)

# ============================================================
# Dictionaries
# ============================================================
symptoms_dict = {
    'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2,
    # ... keep all mappings you defined
}

diseases_list = {
    15: 'Fungal infection', 4: 'Allergy',
    # ... keep all mappings you defined
}

# ============================================================
# Helper Function
# ============================================================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']
    ]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [m for m in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [d for d in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']
    wrkout = [w for w in wrkout.values]

    return desc, pre, med, die, wrkout

# ============================================================
# Model Prediction
# ============================================================
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1
    predicted_class = svc.predict([input_vector])[0]
    return diseases_list[predicted_class]

# ============================================================
# Flask Blueprint
# ============================================================
diagnostics_bp = Blueprint("diagnostics", __name__, url_prefix="/diagnostics")

@diagnostics_bp.route("/")
def diagnostics():
    return render_template("diagnostics.html")

@diagnostics_bp.route("/predict", methods=["POST"])
def predict():
    """
    API Endpoint for Disease Prediction
    Expects: JSON => { "symptoms": ["fever", "cough"] }
    Returns: JSON => prediction + details
    """
    try:
        data = request.get_json(force=True)
        patient_symptoms = data.get("symptoms", [])

        if not patient_symptoms or not isinstance(patient_symptoms, list):
            return jsonify({"status": "error", "message": "Invalid symptoms format"}), 400

        # Prediction
        predicted_disease = get_predicted_value(patient_symptoms)

        # Details
        desc, pre, med, die, wrkout = helper(predicted_disease)

        return jsonify({
            "status": "success",
            "prediction": predicted_disease,
            "description": desc,
            "precautions": pre,
            "medications": med,
            "diets": die,
            "workouts": wrkout
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
