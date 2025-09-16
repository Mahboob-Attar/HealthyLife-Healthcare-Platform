# train_model.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

# ======================================================
# Paths
# ======================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))   # script directory
DATASET_DIR = os.path.join(BASE_DIR, "..", "datasets")  # ../datasets relative to script
dataset_path = os.path.join(DATASET_DIR, "Training.csv")

# ======================================================
# Load dataset
# ======================================================
dataset = pd.read_csv(dataset_path)

X = dataset.drop("prognosis", axis=1)
y = dataset["prognosis"]

# Encode target labels
le = LabelEncoder()
Y = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.3, random_state=20
)

# ======================================================
# Train model (SVC)
# ======================================================
svc = SVC(kernel="linear", probability=True)
svc.fit(X_train, y_train)

# ======================================================
# Save model + encoder together
# ======================================================
model_dir = os.path.join(BASE_DIR, "..", "ml-models")
os.makedirs(model_dir, exist_ok=True)   # ✅ Create folder if not exists
model_path = os.path.join(model_dir, "svc.pkl")

with open(model_path, "wb") as f:
    pickle.dump({"model": svc, "encoder": le, "features": X.columns.tolist()}, f)

print(f"✅ Model + Encoder saved as {model_path}")
