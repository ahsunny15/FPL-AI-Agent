# src/models/match_outcome_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# Simulated file path (replace with actual data when available)
MATCH_DATA_PATH = "data/processed/match_stats.csv"
MODEL_PATH = "models/match_outcome_model.pkl"

def train_match_outcome_model():
    df = pd.read_csv(MATCH_DATA_PATH)

    # Create target variable: win/draw/loss
    def get_outcome(row):
        if row["team_goals"] > row["opponent_goals"]:
            return "win"
        elif row["team_goals"] < row["opponent_goals"]:
            return "loss"
        else:
            return "draw"
    
    df["outcome"] = df.apply(get_outcome, axis=1)

    features = ["team_shots", "team_possession", "team_xG", 
                "opp_shots", "opp_possession", "opp_xG"]

    X = df[features]
    y = df["outcome"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Match outcome model saved to {MODEL_PATH}")

    return model

if __name__ == "__main__":
    train_match_outcome_model()

