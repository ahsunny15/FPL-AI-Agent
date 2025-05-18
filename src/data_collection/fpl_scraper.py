# src/data_collection/fpl_scraper.py

import requests
import pandas as pd
import os

FPL_API_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

def fetch_fpl_data(save_path="data/raw/fpl_players.csv"):
    response = requests.get(FPL_API_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from FPL API")

    data = response.json()
    players = data['elements']
    players_df = pd.DataFrame(players)

    # Save to CSV
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    players_df.to_csv(save_path, index=False)
    print(f"Saved FPL player data to {save_path}")

    return players_df

if __name__ == "__main__":
    df = fetch_fpl_data()
    print(df[['first_name', 'second_name', 'now_cost', 'total_points']].head())
