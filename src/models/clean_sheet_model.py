# src/models/clean_sheet_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

FEATURE_PATH = "data/processed/fpl_features.csv"
MODEL_PATH = "models/clean_sheet_model.pkl"

def train_clean_sheet_model():
    df = pd.read_csv(FEATURE_PATH)

    # Create binary target: likely to get clean sheet
    df["likely_clean_sheet"] = df["clean_sheets"] > 0  # Or threshold like > 0.1 per match

    # Define features
    features = [
        "total_points", "minutes", "points_per_million", 
        "cost", "clean_sheets", "play_chance"
    ]
    df["play_chance"] = df["play_chance"].fillna(100)

    X = df[features]
    y = df["likely_clean_sheet"]

    # Train/test split
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
    print(f"✅ Clean sheet model saved to {MODEL_PATH}")

    return model

if __name__ == "__main__":
    train_clean_sheet_model()
