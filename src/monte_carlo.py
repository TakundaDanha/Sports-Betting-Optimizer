import pandas as pd
import numpy as np
import os

def simulate_betting(bets_df, strategy="flat", initial_bankroll=1000, flat_bet_size=10, n_simulations=10000):
    bankroll = initial_bankroll
    bankroll_progression = [bankroll]

    # Shuffle bets to simulate randomness
    bets = bets_df.sample(frac=1).reset_index(drop=True)

    for i in range(min(n_simulations, len(bets))):
        bet = bets.loc[i]

        odds = bet[f"{bet['bet_type']}_odds"]
        ev = bet["expected_value"]

        # For Kelly: use implied probability as edge estimate
        # Here we use normalized implied probabilities from transform.py
        p = bet[f"{bet['bet_type']}_prob"]

        if strategy == "flat":
            wager = flat_bet_size
        elif strategy == "kelly":
            b = odds - 1
            q = 1 - p
            kelly_fraction = (b * p - q) / b
            wager = bankroll * max(kelly_fraction, 0)  # no negative bets
        else:
            raise ValueError("Strategy must be 'flat' or 'kelly'")

        wager = min(wager, bankroll)  # can't bet more than you have

        # Simulate bet outcome: win with probability p
        if np.random.rand() < p:
            bankroll += wager * (odds - 1)  # winnings
        else:
            bankroll -= wager  # lost wager

        bankroll_progression.append(bankroll)

        # Stop if bankrupt
        if bankroll <= 0:
            break

    return bankroll, bankroll_progression

def main():
    input_csv = "data/processed/value_bets.csv"
    df = pd.read_csv(input_csv)

    # We need implied probabilities from transform step to calculate Kelly bet size
    for bet_type in ['home', 'draw', 'away']:
        prob_col = f"{bet_type}_prob"
        if prob_col not in df.columns:
            df[prob_col] = 1 / df[f"{bet_type}_odds"]  # crude estimate

    # Run simulations for both strategies
    final_bankroll_flat, progression_flat = simulate_betting(df, strategy="flat")
    final_bankroll_kelly, progression_kelly = simulate_betting(df, strategy="kelly")

    print(f"Final bankroll (Flat Betting): ${final_bankroll_flat:.2f}")
    print(f"Final bankroll (Kelly Criterion): ${final_bankroll_kelly:.2f}")

    # Save bankroll progression for analysis or plotting
    os.makedirs("data/processed", exist_ok=True)
    pd.DataFrame({
        "flat_betting": progression_flat,
        "kelly_criterion": progression_kelly[:len(progression_flat)]
    }).to_csv("data/processed/bankroll_progression.csv", index=False)

    print("Simulation complete and results saved to data/processed/bankroll_progression.csv")

if __name__ == "__main__":
    main()
