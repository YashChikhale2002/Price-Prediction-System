# config.py - Updated with Authentication
import os
from datetime import timedelta

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///stock_predictor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Model configuration
    SEQUENCE_LENGTH = 60  # Number of days to look back
    PREDICTION_DAYS = 30  # Number of days to predict
    
    # Stock data configuration
    DEFAULT_PERIOD = '1y'  # Default period for fetching stock data
    
    # Model paths
    MODEL_DIR = 'saved_models'
    
    # Login configuration
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # WTF Forms configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Ensure model directory exists
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)