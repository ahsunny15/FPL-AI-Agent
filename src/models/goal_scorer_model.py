# src/models/goal_scorer_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

FEATURE_PATH = "data/processed/fpl_features.csv"
MODEL_PATH = "models/goal_scorer_model.pkl"

def train_goal_model():
    df = pd.read_csv(FEATURE_PATH)

    # Create binary target: is likely to score (1) or not (0)
    df["will_score"] = df["goals_per_90"] > 0.3  # Customize threshold

    # Define features and target
    features = [
        "goals_per_90", "assists_per_90", "points_per_million",
        "cost", "total_points", "minutes"
    ]
    X = df[features]
    y = df["will_score"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved to {MODEL_PATH}")

    return model

if __name__ == "__main__":
    train_goal_model()
