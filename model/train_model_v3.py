# model/train3.py

import pandas as pd
import pickle
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from sklearn.metrics import accuracy_score, classification_report

DATA_CSV = Path(__file__).parent.parent / "data/data.csv"
MODEL_DIR = Path(__file__).parent
MODEL_V3 = MODEL_DIR / "model_v3.pkl"
SCALER_V3 = MODEL_DIR / "scaler_v3.pkl"

def get_clean_data():
    df = pd.read_csv(DATA_CSV)
    df = df.drop(['Unnamed: 32', 'id'], axis=1)
    df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
    return df

def create_and_calibrate_model(df):
    X = df.drop('diagnosis', axis=1)
    y = df['diagnosis']
    
    # scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # base logistic regression
    base_clf = LogisticRegression(max_iter=1000)
    base_clf.fit(X_train, y_train)
    
    # calibrate probabilities
    base_clf = LogisticRegression(C=0.01, max_iter=1000)
    calibrated = CalibratedClassifierCV(
        estimator=base_clf,
        method='sigmoid',     # or 'sigmoid'
        cv=5
    )
    calibrated.fit(X_train, y_train)
    
    # evaluate
    y_pred = calibrated.predict(X_test)
    y_prob = calibrated.predict_proba(X_test)[:,1]
    
    
    print("▶️ Calibrated Model (v3) Accuracy:", accuracy_score(y_test, y_pred))
    print("▶️ Calibrated Model (v3) Classification Report:\n",
          classification_report(y_test, y_pred, target_names=['Benign','Malignant']))
    
    return calibrated, scaler

def main():
    df = get_clean_data()
    model_v3, scaler_v3 = create_and_calibrate_model(df)
    
    # ensure model dir exists
    MODEL_DIR.mkdir(exist_ok=True)
    
    # save new artifacts
    with open(MODEL_V3, 'wb') as f:
        pickle.dump(model_v3, f)
    with open(SCALER_V3, 'wb') as f:
        pickle.dump(scaler_v3, f)
    
    print(f"✅ Saved calibrated model to {MODEL_V3}")
    print(f"✅ Saved scaler to {SCALER_V3}")

if __name__ == "__main__":
    main()
