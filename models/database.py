# models/database.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with predictions
    predictions = db.relationship('PredictionHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def get_prediction_count(self):
        """Get total number of predictions made by user"""
        return len(self.predictions)
    
    def get_recent_predictions(self, limit=5):
        """Get recent predictions by user"""
        return PredictionHistory.query.filter_by(user_id=self.id)\
            .order_by(PredictionHistory.created_at.desc())\
            .limit(limit).all()
    
    def __repr__(self):
        return f'<User {self.username}>'

class PredictionHistory(db.Model):
    """Model to store prediction history"""
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    symbol = db.Column(db.String(10), nullable=False, index=True)
    period = db.Column(db.String(10), nullable=False)
    
    # Prediction data
    current_price = db.Column(db.Float, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    
    # Statistics (stored as JSON)
    historical_stats = db.Column(db.Text)  # JSON string
    prediction_stats = db.Column(db.Text)  # JSON string
    
    # Chart data (stored as JSON)
    historical_chart_data = db.Column(db.Text)  # JSON string
    prediction_chart_data = db.Column(db.Text)  # JSON string
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    model_accuracy = db.Column(db.Float)  # Optional: store model accuracy
    training_epochs = db.Column(db.Integer, default=30)
    
    def set_historical_stats(self, stats_dict):
        """Set historical statistics as JSON"""
        self.historical_stats = json.dumps(stats_dict)
    
    def get_historical_stats(self):
        """Get historical statistics as dictionary"""
        if self.historical_stats:
            return json.loads(self.historical_stats)
        return {}
    
    def set_prediction_stats(self, stats_dict):
        """Set prediction statistics as JSON"""
        self.prediction_stats = json.dumps(stats_dict)
    
    def get_prediction_stats(self):
        """Get prediction statistics as dictionary"""
        if self.prediction_stats:
            return json.loads(self.prediction_stats)
        return {}
    
    def set_historical_chart_data(self, chart_data):
        """Set historical chart data as JSON"""
        self.historical_chart_data = json.dumps(chart_data)
    
    def get_historical_chart_data(self):
        """Get historical chart data as dictionary"""
        if self.historical_chart_data:
            return json.loads(self.historical_chart_data)
        return {}
    
    def set_prediction_chart_data(self, chart_data):
        """Set prediction chart data as JSON"""
        self.prediction_chart_data = json.dumps(chart_data)
    
    def get_prediction_chart_data(self):
        """Get prediction chart data as dictionary"""
        if self.prediction_chart_data:
            return json.loads(self.prediction_chart_data)
        return {}
    
    def get_sentiment(self):
        """Get market sentiment based on change percentage"""
        if self.change_percent > 5:
            return {'sentiment': 'Very Bullish', 'class': 'text-green-400', 'icon': 'fa-smile'}
        elif self.change_percent > 0:
            return {'sentiment': 'Bullish', 'class': 'text-blue-400', 'icon': 'fa-thumbs-up'}
        elif self.change_percent > -5:
            return {'sentiment': 'Neutral', 'class': 'text-yellow-400', 'icon': 'fa-minus'}
        else:
            return {'sentiment': 'Bearish', 'class': 'text-red-400', 'icon': 'fa-arrow-down'}
    
    def get_age(self):
        """Get how long ago this prediction was made"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    
    def __repr__(self):
        return f'<PredictionHistory {self.symbol} by {self.user.username}>'