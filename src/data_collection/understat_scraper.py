import requests
import json
import pandas as pd
import os
from bs4 import BeautifulSoup

def get_team_match_data(team_name, season="2023"):
    url = f"https://understat.com/team/{team_name}/{season}"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    
    scripts = soup.find_all("script")
    for script in scripts:
        if "matchesData" in script.text:
            json_data = script.text.split("('")[1].split("')")[0]
            json_data = json_data.encode('utf8').decode('unicode_escape')
            data = json.loads(json_data)
            return data
    return None

def process_team_data(team_name, season="2023"):
    raw_data = get_team_match_data(team_name, season)
    if not raw_data:
        print(f"⚠️ No data found for {team_name}")
        return pd.DataFrame()
    
    records = []
    for match in raw_data:
        records.append({
            "team_name": team_name,
            "opponent_name": match['h']['title'] if match['isHome'] == 'false' else match['a']['title'],
            "team_goals": int(match['goals']),
            "opponent_goals": int(match['goalsOpponent']),
            "team_xG": float(match['xG']),
            "opp_xG": float(match['xGA']),
            "team_possession": float(match['ppda']['att']) if match['ppda'] else 0,
            "opp_possession": float(match['ppda_allowed']['att']) if match['ppda_allowed'] else 0,
        })

    return pd.DataFrame(records)

def save_combined_team_data(teams, season="2023"):
    all_matches = []
    for team in teams:
        print(f"🔄 Fetching data for {team}...")
        team_data = process_team_data(team, season)
        all_matches.append(team_data)

    df = pd.concat(all_matches, ignore_index=True)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/match_stats.csv", index=False)
    print("✅ Saved match data to data/processed/match_stats.csv")

if __name__ == "__main__":
    # List of Premier League teams (can be updated)
    teams = [
        "Arsenal", "Manchester_City", "Liverpool", "Tottenham", "Chelsea", 
        "Manchester_United", "Newcastle_United", "Brighton", "Aston_Villa", "Brentford"
    ]
    save_combined_team_data(teams, season="2023")
