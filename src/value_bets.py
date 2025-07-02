import pandas as pd
import os

def calculate_ev(row, bet_type):
    # stake fixed at 1 unit
    stake = 1
    
    # odds for the bet
    odds = row[f"{bet_type}_odds"]
    
    # true probability approx: 1 if result matches bet, else 0
    p_true = 1 if row["result"].lower() == bet_type else 0
    
    # Expected Value formula
    ev = (p_true * (odds * stake)) - ((1 - p_true) * stake)
    return ev

def identify_value_bets(input_csv="data/processed/match_odds_processed.csv",
                        output_csv="data/processed/value_bets.csv"):
    df = pd.read_csv(input_csv)
    
    # Calculate EV for each bet type
    df["ev_home"] = df.apply(lambda row: calculate_ev(row, "home"), axis=1)
    df["ev_draw"] = df.apply(lambda row: calculate_ev(row, "draw"), axis=1)
    df["ev_away"] = df.apply(lambda row: calculate_ev(row, "away"), axis=1)

    # Melt to long format to easily filter positive EV bets
    # Instead of melting only ev columns, add odds to the melt
    ev_long = df.melt(
        id_vars=["match_id", "home_team", "away_team", "start_time", "result",
                "home_odds", "draw_odds", "away_odds"],
        value_vars=["ev_home", "ev_draw", "ev_away"],
        var_name="bet_type",
        value_name="expected_value"
    )


    # Keep only positive EV bets
    positive_ev_bets = ev_long[ev_long["expected_value"] > 0].copy()

    # Clean bet_type naming
    positive_ev_bets["bet_type"] = positive_ev_bets["bet_type"].str.replace("ev_", "")
    
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    positive_ev_bets.to_csv(output_csv, index=False)

    print(f"Identified {len(positive_ev_bets)} positive EV bets saved to {output_csv}")

if __name__ == "__main__":
    identify_value_bets()
