import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_model(df, predictions, initial_balance=1000, risk_per_trade=0.01):
    """
    Simulate trading based on predictions.
    predictions: numpy array of predicted normalized close prices.
    df: original dataframe with 'close' price.
    """
    # Assuming predictions correspond to the last 'len(predictions)' rows of df
    df_test = df.iloc[-len(predictions):].copy()
    df_test['pred_close'] = predictions
    
    # Simple strategy: 
    # If predicted next close > current close, BUY
    # If predicted next close < current close, SELL
    
    # We need to shift predictions to compare with the "next" expected close
    df_test['current_close'] = df_test['close']
    # 'pred_close' is the prediction for the CURRENT candle's close made by the previous 60.
    # So we compare 'pred_close' with 'current_close' to see if it was accurate.
    # To trade, we need the prediction for the NEXT candle.
    
    balance = initial_balance
    equity_curve = [balance]
    trades = []
    
    for i in range(len(df_test) - 1):
        # Current price
        current_price = df_test.iloc[i]['close']
        # Prediction for NEXT candle
        # In our LSTM setup, y[i] is the close of X[i].
        # So pred[i+1] is the prediction for close[i+1].
        predicted_next_price = df_test.iloc[i+1]['pred_close']
        actual_next_price = df_test.iloc[i+1]['close']
        
        # Decide trade direction
        # Note: This is a very simplified model.
        if predicted_next_price > current_price:
            # BUY
            profit = (actual_next_price - current_price) / current_price * balance * risk_per_trade
            balance += profit
        elif predicted_next_price < current_price:
            # SELL
            profit = (current_price - actual_next_price) / current_price * balance * risk_per_trade
            balance += profit
            
        equity_curve.append(balance)
        trades.append(profit)
        
    return equity_curve, trades

if __name__ == "__main__":
    print("Backtester script created. Requires trained model predictions to run fully.")
    # This will be integrated into a larger script later.
