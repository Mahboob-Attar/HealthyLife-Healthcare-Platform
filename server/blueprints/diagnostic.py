import os
import pickle
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from pathlib import Path

# PATH SETUP (FINAL & CORRECT)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_DIR = PROJECT_ROOT / "datasets"
MODEL_DIR = PROJECT_ROOT / "server" / "ml-models"


# LOAD HELPER DATASETS (FOR UI CONTENT)
description = pd.read_csv(os.path.join(DATASET_DIR, "description.csv"))
precautions = pd.read_csv(os.path.join(DATASET_DIR, "precautions_df.csv"))
medications = pd.read_csv(os.path.join(DATASET_DIR, "medications.csv"))
diets = pd.read_csv(os.path.join(DATASET_DIR, "diets.csv"))
workout = pd.read_csv(os.path.join(DATASET_DIR, "workout_df.csv"))


# LOAD TRAINED MODEL + FEATURES
with open(os.path.join(MODEL_DIR, "svc.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_DIR, "features.pkl"), "rb") as f:
    FEATURES = pickle.load(f)   # list of 30 symptoms (training order)


# HELPER FUNCTIONS
def normalize(symptom: str) -> str:
    return symptom.strip().lower().replace(" ", "_")


def build_input_vector(user_symptoms):
    user_symptoms = {normalize(s) for s in user_symptoms}
    return [1 if feature in user_symptoms else 0 for feature in FEATURES]


def get_disease_details(disease):
    desc = description[description["Disease"] == disease]["Description"].values
    pre = precautions[precautions["Disease"] == disease][
        ["Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"]
    ].values
    med = medications[medications["Disease"] == disease]["Medication"].tolist()
    die = diets[diets["Disease"] == disease]["Diet"].tolist()
    wrk = workout[workout["disease"] == disease]["workout"].tolist()

    return {
        "description": desc[0] if len(desc) else "No description available",
        "precautions": pre[0].tolist() if len(pre) else ["No data available"],
        "medications": med if med else ["No data available"],
        "diets": die if die else ["No data available"],
        "workouts": wrk if wrk else ["No data available"]
    }


# FLASK BLUEPRINT
diagnostic_bp = Blueprint("diagnostic", __name__, url_prefix="/diagnostic")


@diagnostic_bp.route("/")
def diagnostic():
    return render_template("diagnostic.html")


@diagnostic_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms") if data else None

    if not symptoms or not isinstance(symptoms, list):
        return jsonify({
            "status": "error",
            "message": "Please provide a valid list of symptoms."
        })
        
    if len(symptoms) < 3:
        return jsonify({
            "status": "error",
            "message": "Please enter at least 2–3 symptoms for accurate prediction."
        })

    # build input for model
    input_vector = build_input_vector(symptoms)
    input_df = pd.DataFrame([input_vector], columns=FEATURES)

    # predict
    predicted_disease = model.predict(input_df)[0]
    confidence = max(model.predict_proba(input_df)[0]) * 100

    details = get_disease_details(predicted_disease)

    return jsonify({
        "status": "success",
        "prediction": predicted_disease,
        "confidence": round(confidence, 2),
        "description": details["description"],
        "precautions": details["precautions"],
        "medications": details["medications"],
        "diets": details["diets"],
        "workouts": details["workouts"]
    })
