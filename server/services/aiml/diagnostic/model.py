from pathlib import Path
import pandas as pd
import pickle

class DiagnosticModel:

    # ---- PATH SETUP ----
    PROJECT_ROOT = Path(__file__).resolve().parents[4]
    DATASET_DIR = PROJECT_ROOT / "datasets"
    MODEL_DIR = PROJECT_ROOT / "server" / "ml-models"

    # ---- VALIDATION (OPTIONAL BUT USEFUL) ----
    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset folder not found at: {DATASET_DIR}")

    if not MODEL_DIR.exists():
        raise FileNotFoundError(f"Model folder not found at: {MODEL_DIR}")

    # ---- LOAD DATASETS ----
    description = pd.read_csv(DATASET_DIR / "description.csv")
    precautions = pd.read_csv(DATASET_DIR / "precautions_df.csv")
    medications = pd.read_csv(DATASET_DIR / "medications.csv")
    diets = pd.read_csv(DATASET_DIR / "diets.csv")
    workout = pd.read_csv(DATASET_DIR / "workout_df.csv")

    # ---- LOAD MODEL FILES ----
    with open(MODEL_DIR / "svc.pkl", "rb") as f:
        model = pickle.load(f)

    with open(MODEL_DIR / "features.pkl", "rb") as f:
        FEATURES = pickle.load(f)



    @staticmethod
    def normalize(symptom: str):
        return symptom.strip().lower().replace(" ", "_")

    @staticmethod
    def build_input_vector(user_symptoms):
        user = {DiagnosticModel.normalize(s) for s in user_symptoms}
        return [1 if feature in user else 0 for feature in DiagnosticModel.FEATURES]

    @staticmethod
    def predict(input_vector):
        df = pd.DataFrame([input_vector], columns=DiagnosticModel.FEATURES)
        prediction = DiagnosticModel.model.predict(df)[0]
        confidence = max(DiagnosticModel.model.predict_proba(df)[0]) * 100
        return prediction, confidence

    @staticmethod
    def get_disease_details(disease):
        desc = DiagnosticModel.description[DiagnosticModel.description["Disease"] == disease]["Description"].values
        pre = DiagnosticModel.precautions[DiagnosticModel.precautions["Disease"] == disease][
            ["Precaution_1", "Precaution_2", "Precaution_3", "Precaution_4"]
        ].values
        med = DiagnosticModel.medications[DiagnosticModel.medications["Disease"] == disease]["Medication"].tolist()
        die = DiagnosticModel.diets[DiagnosticModel.diets["Disease"] == disease]["Diet"].tolist()
        wrk = DiagnosticModel.workout[DiagnosticModel.workout["disease"] == disease]["workout"].tolist()

        return {
            "description": desc[0] if len(desc) else "No description available",
            "precautions": pre[0].tolist() if len(pre) else ["No data available"],
            "medications": med if med else ["No data available"],
            "diets": die if die else ["No data available"],
            "workouts": wrk if wrk else ["No data available"]
        }
