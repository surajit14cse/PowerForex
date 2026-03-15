# AI-Powered Forex Prediction & Auto-Trading System Development Plan

This document outlines the step-by-step development process for the Python-based automated Forex trading system as specified in `implement.text`.

## Phase 1: Environment & Project Setup
*   **Initialize Project:** Create a structured directory (e.g., `src/data`, `src/models`, `src/trading`).
*   **Dependency Management:** Create a `requirements.txt` with `pandas`, `numpy`, `tensorflow`, `scikit-learn`, `MetaTrader5`, and `matplotlib`.
*   **MT5 Connection Test:** Verification script to ensure Python can communicate with the MetaTrader 5 terminal.

## Phase 2: Data Acquisition & Feature Engineering
*   **Data Downloader:** Script to fetch historical OHLCV data for specific symbols (e.g., EURUSD) across multiple timeframes.
*   **Indicator Engine:** Implement a module to calculate:
    *   **Trend:** SMA (20, 50, 200), EMA.
    *   **Momentum:** RSI, MACD.
    *   **Volatility:** Bollinger Bands, ATR.
*   **Storage:** Save processed datasets as CSVs for offline model training.

## Phase 3: Data Preprocessing for Deep Learning
*   **Normalization:** Implement `MinMaxScaler` to fit features within the [0, 1] range.
*   **Sequence Generator:** Create a sliding window function (e.g., use 60 past candles to predict the next 1) to format data for the LSTM input layer.

## Phase 4: LSTM Model Development
*   **Architecture Design:** Build a Sequential model with:
    *   Stacked LSTM layers (50-100 units).
    *   Dropout layers (0.2) to prevent overfitting.
    *   Dense output layer for price prediction.
*   **Training Pipeline:** Split data into training/validation sets and implement early stopping to optimize training time.

## Phase 5: Backtesting & Validation
*   **Simulation Engine:** A script that "trades" on historical data using model predictions.
*   **Metrics:** Calculate Accuracy, Sharpe Ratio, Max Drawdown, and Win/Loss ratio.
*   **Visualization:** Plot predicted vs. actual prices to verify model "fit."

## Phase 6: Live Trading Logic & Risk Management
*   **Execution Module:** Connect predictions to MT5 `order_send` functions.
*   **Risk Layer:** Implement the mandatory rules:
    *   **1% Risk per Trade:** Dynamic lot sizing based on account balance.
    *   **Hard Stop Loss/Take Profit:** Attached to every order.
    *   **Global Drawdown Kill-switch:** Stop all trading if daily loss exceeds 3%.
*   **Main Loop:** A real-time monitor that waits for candle closes, runs the prediction, and manages open positions.

---

## Technical Stack
*   **Language:** Python 3.10+
*   **AI:** TensorFlow / Keras (LSTM)
*   **Data:** Pandas, NumPy, Scikit-learn
*   **Execution:** MetaTrader5 Python API
*   **Backtesting:** yfinance (optional)
