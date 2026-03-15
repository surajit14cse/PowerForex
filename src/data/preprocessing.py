import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

SCALER_PATH = "src/models/scaler.pkl"

def preprocess_for_lstm(df, window_size=60, feature_cols=None, fit_new_scaler=True):
    """
    Scale data and create windowed sequences for LSTM.
    """
    if feature_cols is None:
        feature_cols = [
            'open', 'high', 'low', 'close', 'tick_volume',
            'SMA_20', 'SMA_50', 'SMA_200', 'RSI', 'MACD', 'BB_Upper', 'BB_Lower', 'ATR'
        ]
        
    if fit_new_scaler:
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df[feature_cols])
        # Save the scaler for future use
        os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
        joblib.dump(scaler, SCALER_PATH)
        print(f"New scaler fitted and saved to {SCALER_PATH}")
    else:
        # Load the existing scaler
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            scaled_data = scaler.transform(df[feature_cols])
        else:
            print("Warning: Scaler file not found. Fitting a new one.")
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(df[feature_cols])

    target_idx = feature_cols.index('close')
    
    X = []
    y = []
    
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i-window_size:i, :])
        y.append(scaled_data[i, target_idx])
        
    X = np.array(X)
    y = np.array(y)
    
    return X, y, scaler

if __name__ == "__main__":
    try:
        data = pd.read_csv("src/data/processed_data.csv")
        X, y, scaler = preprocess_for_lstm(data, fit_new_scaler=True)
        print(f"Preprocessing complete.")
        np.save("src/data/X_train.npy", X)
        np.save("src/data/y_train.npy", y)
        print("Sequences saved to .npy files.")
    except FileNotFoundError:
        print("processed_data.csv not found. Run feature_engineering.py first.")
