from flask import Flask, jsonify
import pandas as pd
import pickle
import os

app = Flask(__name__)

# --- Paths ---
DATA_DIR = '../data'
OUTPUTS_DIR = '../outputs'

prices_csv_path = os.path.join(DATA_DIR, 'BrentOilPrices.csv')
events_csv_path = os.path.join(DATA_DIR, 'brent_events.csv')

# --- Load CSVs ---
prices_df = pd.read_csv(prices_csv_path)
events_df = pd.read_csv(events_csv_path)

# --- Convert Date columns safely (mixed formats supported) ---
prices_df['date'] = pd.to_datetime(prices_df['date'], errors='coerce')
events_df['Date'] = pd.to_datetime(events_df['Date'], errors='coerce')

# --- Apply SAME subsampling used in modeling ---
prices_df = prices_df.iloc[::10].reset_index(drop=True)

# --- Load Pickle Files ---
tau_path = os.path.join(OUTPUTS_DIR, 'tau_estimated.pkl')
mu_path = os.path.join(OUTPUTS_DIR, 'mu_posterior.pkl')

with open(tau_path, 'rb') as f:
    tau_estimated = pickle.load(f)

with open(mu_path, 'rb') as f:
    mu_samples = pickle.load(f)

# --- Safe index cleaning ---
tau_estimated_clean = [min(int(idx), len(prices_df)-1) for idx in tau_estimated]

# Convert change point indices to dates
cp_dates = [
    prices_df.iloc[idx]['date'].strftime('%Y-%m-%d')
    for idx in tau_estimated_clean
]

# --- API Endpoints ---

@app.route("/api/prices", methods=["GET"])
def get_prices():
    return prices_df.to_json(orient="records", date_format="iso")

@app.route("/api/events", methods=["GET"])
def get_events():
    return events_df.to_json(orient="records", date_format="iso")

@app.route("/api/regime_means", methods=["GET"])
def get_regime_means():
    means = mu_samples.mean(axis=(0, 1)).tolist()
    return jsonify({"regime_means": means})

@app.route("/api/change_points", methods=["GET"])
def get_change_points():
    return jsonify({"change_points": cp_dates})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
