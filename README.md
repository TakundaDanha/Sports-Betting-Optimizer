# 🧠 Sports Betting Odds Optimizer

This project simulates and analyzes betting odds to identify high-value bets and test betting strategies using Monte Carlo simulations.

## 📊 Problem

In sports betting, identifying "value bets" (where the bookmaker underestimates the true odds) can lead to long-term profitability. This project simulates real-time odds data and calculates the expected value (EV) of different bets. It also includes a simulation to test bankroll growth under different strategies.

## 🛠️ Tech Stack

- Python (pandas, numpy, requests)
- PySpark (for processing odds at scale)
- Streamlit (optional dashboard)
- Monte Carlo Simulation
- JSON / CSV for data

## 🧩 Components

- **Ingestion**: Simulated or scraped data from bookmakers
- **Transformation**: Calculate implied probabilities, normalize odds
- **Value Bet Detection**: Compare implied vs. true odds
- **Simulation**: Test performance of flat betting vs Kelly Criterion over 1000s of iterations
- **Dashboard**: Visualize results and compare strategies

## 🚀 To Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Simulate or scrape odds:
    ```bash
    python src/ingest.py
    ```

3. Run value detection + simulation:
    ```bash
    python src/value_bets.py
    python src/monte_carlo.py
    ```

4. Launch dashboard (optional):
    ```bash
    streamlit run src/app.py
    ```

## 📂 Folder Structure

sports-betting-optimizer/
├── data/
├── notebooks/
├── src/
├── requirements.txt
├── README.md


## ✅ Goals

- Identify profitable betting strategies
- Learn to handle noisy real-world data
- Explore the relationship between implied probability and risk
