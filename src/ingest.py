import os
import json
import random
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd

# Set up faker and teams
fake = Faker()
Faker.seed(42)
random.seed(42)

TEAMS = [
    "Arsenal", "Chelsea", "Liverpool", "Man City", "Man United",
    "Spurs", "Newcastle", "Everton", "West Ham", "Leeds"
]

def generate_match(match_id):
    home, away = random.sample(TEAMS, 2)
    start_time = fake.date_time_between(start_date="now", end_date="+7d")
    
    # Generate odds
    home_odds = round(random.uniform(1.8, 3.0), 2)
    draw_odds = round(random.uniform(2.5, 4.5), 2)
    away_odds = round(random.uniform(2.0, 3.5), 2)

    # Choose result based on inverse odds probabilities
    probs = {
        "Home": 1 / home_odds,
        "Draw": 1 / draw_odds,
        "Away": 1 / away_odds
    }
    total = sum(probs.values())
    for k in probs:
        probs[k] /= total
    result = random.choices(list(probs.keys()), weights=probs.values(), k=1)[0]

    return {
        "match_id": match_id,
        "home_team": home,
        "away_team": away,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "home_odds": home_odds,
        "draw_odds": draw_odds,
        "away_odds": away_odds,
        "result": result
    }

def generate_matches(n_matches=100):
    return [generate_match(f"M{str(i+1).zfill(3)}") for i in range(n_matches)]

def main():
    matches = generate_matches(100)
    df = pd.DataFrame(matches)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/match_odds.csv", index=False)

    with open("data/raw/match_odds.json", "w") as f:
        json.dump(matches, f, indent=4)

    print("Generated 100 simulated matches.")

if __name__ == "__main__":
    main()
