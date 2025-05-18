# src/data_processing/clean_fpl_data.py

import pandas as pd
import os

RAW_PATH = "data/raw/fpl_players.csv"
CLEANED_PATH = "data/processed/fpl_cleaned.csv"

def clean_fpl_data(raw_path=RAW_PATH, cleaned_path=CLEANED_PATH):
    df = pd.read_csv(raw_path)

    # Select useful columns
    selected_cols = [
        "first_name", "second_name", "team", "now_cost",
        "total_points", "goals_scored", "assists", "clean_sheets",
        "minutes", "selected_by_percent", "chance_of_playing_next_round"
    ]

    df = df[selected_cols]

    # Rename for readability
    df.rename(columns={
        "first_name": "first",
        "second_name": "last",
        "now_cost": "cost",
        "selected_by_percent": "popularity",
        "chance_of_playing_next_round": "play_chance"
    }, inplace=True)

    # Convert cost from integer to float (FPL cost is x10 in API)
    df["cost"] = df["cost"] / 10

    # Save cleaned file
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    df.to_csv(cleaned_path, index=False)
    print(f"✅ Cleaned data saved to {cleaned_path}")

    return df

if __name__ == "__main__":
    df = clean_fpl_data()
    print(df.head())
