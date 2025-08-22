import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import os
from config import Config

class StockPredictor:
    def __init__(self, sequence_length=60, n_features=1):
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
        self._build_model()
    
    def _build_model(self):
        """Build the LSTM model architecture"""
        self.model = Sequential([
            # First LSTM layer
            LSTM(units=50, return_sequences=True, 
                 input_shape=(self.sequence_length, self.n_features)),
            Dropout(0.2),
            
            # Second LSTM layer
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            
            # Third LSTM layer
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            
            # Output layer
            Dense(units=1)
        ])
        
        # Compile the model
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mean_squared_error',
            metrics=['mae']
        )
    
    def train(self, X_train, y_train, epochs=50, batch_size=32, validation_split=0.1):
        """Train the LSTM model"""
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1,
            shuffle=False
        )
        return history
    
    def predict(self, X_test, scaler):
        """Make predictions on test data"""
        if len(X_test) == 0:
            return np.array([])
        
        # Ensure proper shape for LSTM
        if len(X_test.shape) == 2:
            X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
        
        predictions_scaled = self.model.predict(X_test, verbose=0)
        predictions = scaler.inverse_transform(predictions_scaled)
        return predictions.flatten()
    
    def predict_future(self, last_sequence, scaler, days=30):
        """Predict future stock prices"""
        predictions = []
        current_sequence = last_sequence.copy().flatten()
        
        for _ in range(days):
            # Ensure we have the right sequence length
            if len(current_sequence) > self.sequence_length:
                current_sequence = current_sequence[-self.sequence_length:]
            elif len(current_sequence) < self.sequence_length:
                # Pad with last value if needed
                pad_length = self.sequence_length - len(current_sequence)
                current_sequence = np.concatenate([
                    np.full(pad_length, current_sequence[0]), 
                    current_sequence
                ])
            
            # Reshape for prediction (1, sequence_length, 1)
            prediction_input = current_sequence.reshape((1, self.sequence_length, 1))
            
            # Make prediction
            next_price_scaled = self.model.predict(prediction_input, verbose=0)
            
            # Inverse transform to get actual price
            next_price = scaler.inverse_transform(next_price_scaled)[0, 0]
            predictions.append(next_price)
            
            # Update sequence for next prediction
            current_sequence = np.append(current_sequence[1:], next_price_scaled[0, 0])
        
        return np.array(predictions)
    
    def save_model(self, symbol):
        """Save the trained model"""
        model_path = os.path.join(Config.MODEL_DIR, f'{symbol}_model.h5')
        self.model.save(model_path)
        return model_path
    
    def load_model(self, symbol):
        """Load a saved model"""
        model_path = os.path.join(Config.MODEL_DIR, f'{symbol}_model.h5')
        if os.path.exists(model_path):
            self.model = tf.keras.models.load_model(model_path)
            return True
        return False