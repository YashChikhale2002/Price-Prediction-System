import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Model configuration
    SEQUENCE_LENGTH = 60  # Number of days to look back
    PREDICTION_DAYS = 30  # Number of days to predict
    
    # Stock data configuration
    DEFAULT_PERIOD = '5y'  # Default period for fetching stock data
    
    # Model paths
    MODEL_DIR = 'saved_models'
    
    # Ensure model directory exists
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)