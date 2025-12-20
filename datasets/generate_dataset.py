import pandas as pd
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "disease_training.csv"

symptoms = [
    "fever","high_fever","chills","sweating",
    "cough","dry_cough","wet_cough","cold","runny_nose","sore_throat",
    "headache","fatigue","body_pain","joint_pain","muscle_pain",
    "nausea","vomiting","diarrhea","abdominal_pain","loss_of_appetite",
    "breathlessness","chest_pain","palpitations","dizziness",
    "itching","skin_rash","swelling","weight_loss","dehydration","weakness"
]

disease_patterns = {
    "Flu": ["fever","cough","fatigue","body_pain","headache","sore_throat"],
    "Common Cold": ["cold","runny_nose","cough","sore_throat"],
    "Typhoid": ["high_fever","headache","fatigue","loss_of_appetite","abdominal_pain"],
    "Allergy": ["itching","skin_rash","runny_nose","swelling"],
    "Dengue": ["high_fever","joint_pain","muscle_pain","chills","weakness"],
    "COVID-19": ["fever","dry_cough","fatigue","breathlessness"],
    "Sore Throat": ["sore_throat","cough","headache"],
    "Gastroenteritis": ["diarrhea","vomiting","abdominal_pain","dehydration"],
    "Heart Disease": ["chest_pain","palpitations","breathlessness","dizziness"],
    "Viral Fever": ["fever","fatigue","body_pain","weakness"]
}

rows = []

for disease, base_symptoms in disease_patterns.items():
    for _ in range(150):  # 10 diseases × 150 rows = 1500 rows
        row = {s: 0 for s in symptoms}

        for s in base_symptoms:
            row[s] = 1

        # small realistic noise
        for s in random.sample(symptoms, random.randint(1, 3)):
            row[s] = 1

        row["disease"] = disease
        rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print("disease_training.csv created")
print("Rows:", len(df))
