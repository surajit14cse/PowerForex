import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np

def build_lstm_model(input_shape):
    """
    Build the LSTM Sequential model.
    input_shape should be (window_size, n_features)
    """
    model = Sequential([
        Input(shape=input_shape),
        # First LSTM layer
        LSTM(units=100, return_sequences=True),
        Dropout(0.2),
        
        # Second LSTM layer
        LSTM(units=100, return_sequences=False),
        Dropout(0.2),
        
        # Dense layers for final prediction
        Dense(units=50, activation='relu'),
        Dense(units=1) # Predicting the next Close price
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(X, y, epochs=50, batch_size=32):
    """
    Split data and train the model.
    """
    # Split data (80/20)
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    # Define Early Stopping to prevent overfitting
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    
    # Build model
    model = build_lstm_model(input_shape=(X.shape[1], X.shape[2]))
    
    # Train
    print("Starting training...")
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_val, y_val),
        callbacks=[early_stopping],
        verbose=1
    )
    
    return model, history

if __name__ == "__main__":
    # Test on the saved .npy files
    try:
        X = np.load("src/data/X_train.npy")
        y = np.load("src/data/y_train.npy")
        
        model, history = train_model(X, y, epochs=5) # Few epochs for testing
        
        model.save("src/models/forex_model.h5")
        print("Model saved to src/models/forex_model.h5")
    except FileNotFoundError:
        print("X_train.npy/y_train.npy not found. Run preprocessing.py first.")
