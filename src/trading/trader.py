import MetaTrader5 as mt5
import pandas as pd
import numpy as np

def place_order(symbol, order_type, lot, price, sl, tp):
    """
    Sends an order to MetaTrader 5.
    """
    if not mt5.initialize():
        print("MT5 initialization failed for order.")
        return False
    
    # Map order types
    mt5_order_type = mt5.ORDER_TYPE_BUY if order_type == 'BUY' else mt5.ORDER_TYPE_SELL
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5_order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456, # Unique ID for this bot
        "comment": "AI Bot Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    # Send order
    result = mt5.order_send(request)
    if result is None:
        print(f"Order failed for {symbol}. Error: {mt5.last_error()}")
        return False
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order retcode error: {result.retcode}")
        return False
        
    print(f"Order placed successfully! Ticket: {result.order}")
    return True

def calculate_lot_size(balance, risk_percent, stop_loss_pips):
    """
    Calculate lot size based on account balance and risk.
    Example: Risk 1% of $1000 = $10.
    """
    risk_amount = balance * risk_percent
    # Simplistic calculation: $10 risk / (stop_loss_pips * point_value)
    # This requires detailed knowledge of the symbol's contract size.
    # Defaulting to 0.01 lot for safety in this placeholder.
    return 0.01

def check_drawdown(initial_daily_balance, current_balance, max_percent=0.03):
    """
    Checks if the account drawdown has exceeded the daily limit.
    """
    if current_balance < initial_daily_balance * (1 - max_percent):
        print("CRITICAL: Daily drawdown limit reached. Stopping all trading.")
        return True
    return False

if __name__ == "__main__":
    print("Trader script created. Live trading requires full integration with the AI model.")
