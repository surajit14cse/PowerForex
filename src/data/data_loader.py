import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import yfinance as yf
from src.utils.mt5_connection import initialize_mt5

def get_mt5_data(symbol, timeframe, n_candles):
    """
    Fetch historical data from MetaTrader 5 with yfinance fallback.
    """
    if not initialize_mt5():
        print("MT5 initialization failed. Falling back to yfinance...")
        # Map symbol to yfinance format (e.g. EURUSD -> EURUSD=X)
        yf_symbol = f"{symbol}=X" if "=" not in symbol else symbol
        return get_yfinance_data(yf_symbol, timeframe, period="1mo")
    
    # Get timeframe mapping
    tf_mapping = {
        '5m': mt5.TIMEFRAME_M5,
        '15m': mt5.TIMEFRAME_M15,
        '1h': mt5.TIMEFRAME_H1,
        '4h': mt5.TIMEFRAME_H4,
        '1d': mt5.TIMEFRAME_D1
    }
    
    if timeframe not in tf_mapping:
        print(f"Timeframe {timeframe} not supported.")
        mt5.shutdown()
        return None
    
    print(f"Downloading {n_candles} candles for {symbol} ({timeframe}) from MT5...")
    
    rates = mt5.copy_rates_from_pos(symbol, tf_mapping[timeframe], 0, n_candles)
    
    if rates is None:
        print(f"Failed to copy rates for {symbol}. Error: {mt5.last_error()}. Trying yfinance...")
        yf_symbol = f"{symbol}=X" if "=" not in symbol else symbol
        data = get_yfinance_data(yf_symbol, timeframe, period="1mo")
        mt5.shutdown()
        return data
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    mt5.shutdown()
    return df

def get_yfinance_data(symbol, timeframe, period="2y"):
    """
    Fetch historical data from yfinance.
    """
    print(f"Downloading {symbol} data from yfinance (Period: {period}, Interval: {timeframe})...")
    
    # Mapping yfinance intervals
    yf_tf_mapping = {
        '5m': '5m',
        '15m': '15m',
        '1h': '1h',
        '4h': '1h', # yf doesn't directly support 4h in some regions/apis, using 1h
        '1d': '1d'
    }
    
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period, interval=yf_tf_mapping.get(timeframe, '1h'))
    
    df.reset_index(inplace=True)
    df.rename(columns={'Date': 'time', 'Datetime': 'time', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'tick_volume'}, inplace=True)
    
    return df

if __name__ == "__main__":
    # Example usage (testing with yfinance first)
    symbol = "EURUSD=X" # For yfinance forex
    data = get_yfinance_data(symbol, "1h", period="1y")
    
    if data is not None and not data.empty:
        print(f"Successfully downloaded {len(data)} rows.")
        data.to_csv("src/data/historical_data.csv", index=False)
        print("Saved to src/data/historical_data.csv")
    else:
        print("Download failed.")
