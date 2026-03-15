import pandas as pd
import numpy as np

def calculate_indicators(df):
    """
    Calculate technical indicators for the dataset.
    Expects df with columns: ['open', 'high', 'low', 'close', 'tick_volume']
    """
    # Ensure columns are float
    for col in ['open', 'high', 'low', 'close', 'tick_volume']:
        df[col] = df[col].astype(float)
        
    # Moving Averages
    df['SMA_20'] = df['close'].rolling(window=20).mean()
    df['SMA_50'] = df['close'].rolling(window=50).mean()
    df['SMA_200'] = df['close'].rolling(window=200).mean()
    
    # RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD (Moving Average Convergence Divergence)
    ema_12 = df['close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_Mid'] = df['close'].rolling(window=20).mean()
    df['BB_Std'] = df['close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Mid'] + (df['BB_Std'] * 2)
    df['BB_Lower'] = df['BB_Mid'] - (df['BB_Std'] * 2)
    
    # Average True Range (ATR) - simple implementation
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['ATR'] = true_range.rolling(14).mean()
    
    # Drop NaN rows created by rolling windows
    df.dropna(inplace=True)
    
    return df

if __name__ == "__main__":
    # Test on the saved historical data
    try:
        data = pd.read_csv("src/data/historical_data.csv")
        data_with_features = calculate_indicators(data)
        print(f"Features added. New shape: {data_with_features.shape}")
        data_with_features.to_csv("src/data/processed_data.csv", index=False)
        print("Saved to src/data/processed_data.csv")
        print(data_with_features.tail())
    except FileNotFoundError:
        print("historical_data.csv not found. Run data_loader.py first.")
