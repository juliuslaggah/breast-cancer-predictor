# train_model.py

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from pathlib import Path

# Load dataset
df = pd.read_csv("data/data.csv")

# Drop irrelevant columns
df.drop(columns=["Unnamed: 32", "id"], inplace=True, errors="ignore")

# Encode target
df["diagnosis"] = df["diagnosis"].map({"M": 1, "B": 0})

# Define features
cytology_features = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
    'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst',
    'compactness_worst', 'concavity_worst', 'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

# Optional: extra imaging features (mock for now)
extra_features = ['volume_cm3', 'mean_area_px', 'surface_area_cm2']
df[extra_features] = np.random.rand(len(df), len(extra_features))  # Add mock values

# Target
y = df["diagnosis"]

# Ensure model directory
model_dir = Path("model")
model_dir.mkdir(exist_ok=True)

# ---- Train Cytology-Only Model (v1) ----
X_v1 = df[cytology_features]
X_v1_train, X_v1_test, y_v1_train, y_v1_test = train_test_split(X_v1, y, test_size=0.2, random_state=42)

scaler_v1 = StandardScaler()
X_v1_train_scaled = scaler_v1.fit_transform(X_v1_train)
X_v1_test_scaled = scaler_v1.transform(X_v1_test)

model_v1 = RandomForestClassifier(n_estimators=100, random_state=42)
model_v1.fit(X_v1_train_scaled, y_v1_train)
y_v1_pred = model_v1.predict(X_v1_test_scaled)

print("\n📊 Cytology-Only Model (v1) Classification Report:\n")
print(classification_report(y_v1_test, y_v1_pred, target_names=["Benign", "Malignant"]))

# Save v1 model and scaler
pickle.dump(model_v1, open(model_dir / "model_v1.pkl", "wb"))
pickle.dump(scaler_v1, open(model_dir / "scaler_v1.pkl", "wb"))

# ---- Train Combined Model (v2) ----
X_v2 = df[cytology_features + extra_features]
X_v2_train, X_v2_test, y_v2_train, y_v2_test = train_test_split(X_v2, y, test_size=0.2, random_state=42)

scaler_v2 = StandardScaler()
X_v2_train_scaled = scaler_v2.fit_transform(X_v2_train)
X_v2_test_scaled = scaler_v2.transform(X_v2_test)

model_v2 = RandomForestClassifier(n_estimators=100, random_state=42)
model_v2.fit(X_v2_train_scaled, y_v2_train)
y_v2_pred = model_v2.predict(X_v2_test_scaled)

print("\n📊 Cytology + Imaging Model (v2) Classification Report:\n")
print(classification_report(y_v2_test, y_v2_pred, target_names=["Benign (0)", "Malignant (1)"]))

# Save v2 model and scaler
pickle.dump(model_v2, open(model_dir / "model_v2.pkl", "wb"))
pickle.dump(scaler_v2, open(model_dir / "scaler_v2.pkl", "wb"))

print("\n✅ Models trained and saved to /model directory.")
