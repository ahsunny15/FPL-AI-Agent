# src/data_processing/feature_engineering.py

import pandas as pd
import os

CLEANED_PATH = "data/processed/fpl_cleaned.csv"
FEATURED_PATH = "data/processed/fpl_features.csv"

def create_features(cleaned_path=CLEANED_PATH, featured_path=FEATURED_PATH):
    df = pd.read_csv(cleaned_path)

    # New features
    df["full_name"] = df["first"] + " " + df["last"]
    df["goals_per_90"] = df["goals_scored"] / (df["minutes"] / 90 + 1e-6)
    df["assists_per_90"] = df["assists"] / (df["minutes"] / 90 + 1e-6)
    df["points_per_million"] = df["total_points"] / (df["cost"] + 1e-6)
    df["is_playing_next"] = df["play_chance"].fillna(100) > 75

    # Save for modeling
    os.makedirs(os.path.dirname(featured_path), exist_ok=True)
    df.to_csv(featured_path, index=False)
    print(f"✅ Features saved to {featured_path}")

    return df

if __name__ == "__main__":
    df = create_features()
    print(df[["full_name", "goals_per_90", "assists_per_90", "points_per_million", "is_playing_next"]].head())
