import os
import pandas as pd

def calculate_implied_probabilities(row):
    return pd.Series({
        "home_prob": 1 / row["home_odds"],
        "draw_prob": 1 / row["draw_odds"],
        "away_prob": 1 / row["away_odds"],
    })

def normalize_probabilities(probs):
    total = probs.sum()
    return probs / total

def transform_odds(input_csv="data/raw/match_odds.csv", output_csv="data/processed/match_odds_processed.csv"):
    df = pd.read_csv(input_csv)

    # Calculate implied probabilities
    prob_cols = ["home_prob", "draw_prob", "away_prob"]
    df_probs = df.apply(calculate_implied_probabilities, axis=1, result_type='expand')

    # Normalize probabilities to remove bookmaker margin
    normalized_probs = df_probs.apply(normalize_probabilities, axis=1, result_type='expand')
    normalized_probs.columns = prob_cols

    # Add normalized probabilities to dataframe
    df = pd.concat([df, normalized_probs], axis=1)

    # Create processed directory 
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"Transformed data saved to {output_csv}")

if __name__ == "__main__":
    transform_odds()
