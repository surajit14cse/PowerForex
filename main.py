import time
import MetaTrader5 as mt5
from src.data.data_loader import get_mt5_data
from src.data.feature_engineering import calculate_indicators
from src.data.preprocessing import preprocess_for_lstm
from src.models.lstm_model import train_model
from src.trading.trader import place_order, calculate_lot_size, check_drawdown
from src.utils.mt5_connection import initialize_mt5
import tensorflow as tf
from tensorflow import keras
import os

# --- Configuration ---
SYMBOL = "EURUSD"
TIMEFRAME = "1h"
LOOKBACK_WINDOW = 60
RISK_PERCENT = 0.01
DRAWDOWN_LIMIT = 0.03
MODEL_PATH = "src/models/forex_model.h5"

def execute_trading_logic(prediction_scaled, last_scaled_close, symbol, mt5_active):
    if not mt5_active:
        return
        
    # Simple logic: If predicted next close > current close, BUY. Else, SELL.
    if prediction_scaled > last_scaled_close:
        signal = "BUY"
    else:
        signal = "SELL"
        
    print(f"Signal Generated: {signal}")
    
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found.")
        return

    lot = 0.01 
    price = symbol_info.ask if signal == "BUY" else symbol_info.bid
    
    point = symbol_info.point
    sl = price - 500 * point if signal == "BUY" else price + 500 * point
    tp = price + 1000 * point if signal == "BUY" else price - 1000 * point

    place_order(symbol, signal, lot, price, sl, tp)

def run_trading_bot():
    print(f"--- Starting AI Trading Bot for {SYMBOL} ({TIMEFRAME}) ---")
    
    mt5_active = initialize_mt5()
    if not mt5_active:
        print(f"MT5 initialization failed. Error: {mt5.last_error()}")
        print("Bot will run in MONITORING MODE (Prediction only, no trading).")
    else:
        print("MT5 successfully initialized. Bot running in LIVE TRADING MODE.")

    if os.path.exists(MODEL_PATH):
        print("Loading existing AI model...")
        model = tf.keras.models.load_model(MODEL_PATH)
    else:
        print("Model not found. Please run a training script first.")
        if mt5_active: mt5.shutdown()
        return

    try:
        while True:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Monitoring {SYMBOL} for new data...")
            
            raw_data = get_mt5_data(SYMBOL, TIMEFRAME, LOOKBACK_WINDOW + 200) 
            if raw_data is None or raw_data.empty:
                print("Failed to fetch data. Retrying in 60 seconds...")
                time.sleep(60)
                continue
            
            df_with_features = calculate_indicators(raw_data)
            X, _, scaler = preprocess_for_lstm(df_with_features, window_size=LOOKBACK_WINDOW, fit_new_scaler=False)
            
            feature_cols = ['open', 'high', 'low', 'close', 'tick_volume', 'SMA_20', 'SMA_50', 'SMA_200', 'RSI', 'MACD', 'BB_Upper', 'BB_Lower', 'ATR']
            last_scaled_close = X[-1, -1, feature_cols.index('close')]
            
            current_window = X[-1].reshape(1, LOOKBACK_WINDOW, X.shape[2])
            prediction_scaled = model.predict(current_window, verbose=0)[0][0]
            
            print(f"Current Price (Scaled): {last_scaled_close:.4f}")
            print(f"Predicted Next Price (Scaled): {prediction_scaled:.4f}")
            
            if mt5_active:
                execute_trading_logic(prediction_scaled, last_scaled_close, SYMBOL, mt5_active)
            else:
                print("Trading skipped (MT5 not connected).")
            
            time.sleep(60) 
            
    except KeyboardInterrupt:
        print("Shutting down bot...")
    finally:
        if mt5_active:
            mt5.shutdown()

if __name__ == "__main__":
    run_trading_bot()
