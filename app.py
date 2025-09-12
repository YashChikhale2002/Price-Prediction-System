# app.py - Final Fixed Version with All Routes Working
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import json
import numpy as np
from models.lstm_model import StockPredictor
from utils.data_fetcher import fetch_stock_data
from utils.data_processor import prepare_data
import pandas as pd
import traceback
from datetime import datetime, timedelta
import os
import re

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-super-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///stock_predictor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Model configuration
app.config['SEQUENCE_LENGTH'] = 60
app.config['PREDICTION_DAYS'] = 30

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Database Models
class User(UserMixin, db.Model):
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
    
    predictions = db.relationship('PredictionHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_prediction_count(self):
        return len(self.predictions)
    
    def get_recent_predictions(self, limit=5):
        return PredictionHistory.query.filter_by(user_id=self.id)\
            .order_by(PredictionHistory.created_at.desc())\
            .limit(limit).all()

class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    symbol = db.Column(db.String(10), nullable=False, index=True)
    period = db.Column(db.String(10), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    predicted_price = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    historical_stats = db.Column(db.Text)
    prediction_stats = db.Column(db.Text)
    historical_chart_data = db.Column(db.Text)
    prediction_chart_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def set_historical_stats(self, stats_dict):
        self.historical_stats = json.dumps(stats_dict)
    
    def get_historical_stats(self):
        return json.loads(self.historical_stats) if self.historical_stats else {}
    
    def set_prediction_stats(self, stats_dict):
        self.prediction_stats = json.dumps(stats_dict)
    
    def get_prediction_stats(self):
        return json.loads(self.prediction_stats) if self.prediction_stats else {}
    
    def set_historical_chart_data(self, chart_data):
        self.historical_chart_data = json.dumps(chart_data)
    
    def get_historical_chart_data(self):
        return json.loads(self.historical_chart_data) if self.historical_chart_data else {}
    
    def set_prediction_chart_data(self, chart_data):
        self.prediction_chart_data = json.dumps(chart_data)
    
    def get_prediction_chart_data(self):
        return json.loads(self.prediction_chart_data) if self.prediction_chart_data else {}
    
    def get_sentiment(self):
        if self.change_percent > 5:
            return {'sentiment': 'Very Bullish', 'class': 'text-green-400', 'icon': 'fa-smile'}
        elif self.change_percent > 0:
            return {'sentiment': 'Bullish', 'class': 'text-blue-400', 'icon': 'fa-thumbs-up'}
        elif self.change_percent > -5:
            return {'sentiment': 'Neutral', 'class': 'text-yellow-400', 'icon': 'fa-minus'}
        else:
            return {'sentiment': 'Bearish', 'class': 'text-red-400', 'icon': 'fa-arrow-down'}
    
    def get_age(self):
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

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
    
    def validate_username(self, username):
        if not re.match(r'^[a-zA-Z0-9_]+$', username.data):
            raise ValidationError('Username can only contain letters, numbers, and underscores')
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('Username already taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered.')

class StockPredictionForm(FlaskForm):
    symbol = StringField('Stock Symbol', validators=[DataRequired(), Length(min=1, max=10)])
    period = SelectField('Analysis Period', choices=[
        ('6mo', '6 Months'), ('1y', '1 Year'), ('2y', '2 Years'), ('5y', '5 Years')
    ], default='1y')
    submit = SubmitField('Generate AI Prediction')

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper function
def create_chart_data(dates, prices, name):
    """Create chart data structure for frontend with robust error handling"""
    try:
        print(f"🔄 Creating chart data for {name}")
        
        if dates is None or prices is None:
            raise ValueError(f"No data available for {name}")
        
        # Convert inputs to lists
        if hasattr(dates, 'tolist'):
            dates_list = dates.tolist()
        elif hasattr(dates, '__iter__'):
            dates_list = list(dates)
        else:
            raise ValueError(f"Invalid dates format for {name}")
        
        if hasattr(prices, 'tolist'):
            prices_list = prices.tolist()
        elif hasattr(prices, '__iter__'):
            prices_list = list(prices)
        else:
            raise ValueError(f"Invalid prices format for {name}")
        
        if len(dates_list) == 0 or len(prices_list) == 0:
            raise ValueError(f"Empty data arrays for {name}")
        
        if len(dates_list) != len(prices_list):
            min_length = min(len(dates_list), len(prices_list))
            dates_list = dates_list[:min_length]
            prices_list = prices_list[:min_length]
        
        # Format dates consistently
        formatted_dates = []
        for date in dates_list:
            if hasattr(date, 'strftime'):
                formatted_dates.append(date.strftime('%Y-%m-%d'))
            elif isinstance(date, str):
                formatted_dates.append(date)
            else:
                formatted_dates.append(str(date))
        
        # Ensure prices are numeric
        formatted_prices = []
        for price in prices_list:
            try:
                formatted_prices.append(float(price))
            except (ValueError, TypeError):
                formatted_prices.append(0.0)
        
        chart_data = {
            'labels': formatted_dates,
            'prices': formatted_prices,
            'name': name,
            'min_price': float(min(formatted_prices)) if formatted_prices else 0.0,
            'max_price': float(max(formatted_prices)) if formatted_prices else 0.0,
            'avg_price': float(sum(formatted_prices) / len(formatted_prices)) if formatted_prices else 0.0
        }
        
        print(f"✅ Chart data created for {name}: {len(formatted_prices)} points")
        return chart_data
    
    except Exception as e:
        print(f"❌ Error creating chart data for {name}: {str(e)}")
        return {
            'labels': ['2025-01-01', '2025-01-02', '2025-01-03'],
            'prices': [100.0, 102.0, 101.0],
            'name': f"{name} (Error)",
            'min_price': 100.0,
            'max_price': 102.0,
            'avg_price': 101.0
        }

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username.data.lower().strip()
        password = form.password.data
        remember = form.remember_me.data
        
        user = None
        if '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()
        
        if user and user.check_password(password) and user.is_active:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.first_name}!', 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username/email or password.', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data.lower().strip(),
                email=form.email.data.lower().strip(),
                first_name=form.first_name.data.strip().title(),
                last_name=form.last_name.data.strip().title(),
                created_at=datetime.utcnow()
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'Registration successful! Welcome, {user.first_name}!', 'success')
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            print(f"Registration error: {str(e)}")
    
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    form = StockPredictionForm()
    recent_predictions = current_user.get_recent_predictions(limit=5)
    total_predictions = current_user.get_prediction_count()
    return render_template('dashboard.html', form=form, recent_predictions=recent_predictions, total_predictions=total_predictions)

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        symbol = request.form.get('symbol', '').upper().strip()
        period = request.form.get('period', '1y')
        
        print(f"🎯 Starting prediction for {symbol} with {period} period (User: {current_user.username})")
        
        if not symbol:
            flash('Please provide a stock symbol', 'error')
            return redirect(url_for('dashboard'))
        
        # Fetch stock data
        print(f"📡 Fetching stock data for {symbol}...")
        stock_data = fetch_stock_data(symbol, period)
        
        if stock_data is None or stock_data.empty:
            print(f"❌ No data found for {symbol}")
            flash(f'Could not fetch data for symbol {symbol}. Please check if the symbol exists.', 'error')
            return redirect(url_for('dashboard'))
        
        print(f"✅ Fetched {len(stock_data)} data points for {symbol}")
        
        if len(stock_data) < app.config['SEQUENCE_LENGTH']:
            flash(f'Insufficient data for {symbol}. Need at least {app.config["SEQUENCE_LENGTH"]} days of data.', 'error')
            return redirect(url_for('dashboard'))
        
        # Prepare data for training
        print("🔄 Preparing data for LSTM training...")
        X_train, y_train, X_test, scaler, last_sequence = prepare_data(stock_data, app.config['SEQUENCE_LENGTH'])
        print(f"✅ Data prepared - Training: {len(X_train)}, Test: {len(X_test)}")
        
        # Create and train model
        print("🧠 Creating and training LSTM model...")
        predictor = StockPredictor(sequence_length=app.config['SEQUENCE_LENGTH'], n_features=1)
        
        print("🏋️ Training neural network...")
        history = predictor.train(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1)
        print("✅ Model training completed")
        
        # Make predictions
        print("🔮 Generating predictions...")
        if len(X_test) > 0:
            test_predictions = predictor.predict(X_test, scaler)
            print(f"✅ Generated {len(test_predictions)} test predictions")
        else:
            test_predictions = np.array([])
        
        future_predictions = predictor.predict_future(last_sequence, scaler, days=app.config['PREDICTION_DAYS'])
        print(f"✅ Generated {len(future_predictions)} future predictions")
        
        if len(future_predictions) == 0:
            raise ValueError("No future predictions generated")
        
        # Prepare data for visualization
        print("📊 Preparing visualization data...")
        historical_prices = stock_data['Close'].values
        historical_dates = stock_data.index
        
        # Create future dates
        last_date = stock_data.index[-1]
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=len(future_predictions),
            freq='B'
        )
        
        # Create chart data
        historical_chart_data = create_chart_data(historical_dates, historical_prices, 'Historical Prices')
        prediction_chart_data = create_chart_data(future_dates, future_predictions, 'AI Predictions')
        
        # Calculate statistics
        historical_stats = {
            'min_price': float(np.min(historical_prices)),
            'max_price': float(np.max(historical_prices)),
            'avg_price': float(np.mean(historical_prices)),
            'volatility': float(np.std(historical_prices))
        }
        
        prediction_stats = {
            'min_prediction': float(np.min(future_predictions)),
            'max_prediction': float(np.max(future_predictions)),
            'avg_prediction': float(np.mean(future_predictions)),
            'trend': 'bullish' if future_predictions[-1] > future_predictions[0] else 'bearish'
        }
        
        # Calculate key metrics
        current_price = float(historical_prices[-1])
        predicted_price = float(future_predictions[-1])
        change_percent = ((predicted_price - current_price) / current_price) * 100
        
        print(f"💰 Current: ${current_price:.2f}, Predicted: ${predicted_price:.2f}, Change: {change_percent:.2f}%")
        
        # Save prediction to database
        try:
            prediction_record = PredictionHistory(
                user_id=current_user.id,
                symbol=symbol,
                period=period,
                current_price=current_price,
                predicted_price=predicted_price,
                change_percent=change_percent
            )
            
            prediction_record.set_historical_stats(historical_stats)
            prediction_record.set_prediction_stats(prediction_stats)
            prediction_record.set_historical_chart_data(historical_chart_data)
            prediction_record.set_prediction_chart_data(prediction_chart_data)
            
            db.session.add(prediction_record)
            db.session.commit()
            print("✅ Prediction saved to database")
        except Exception as e:
            print(f"⚠️ Warning: Could not save prediction: {str(e)}")
            db.session.rollback()
        
        print("🎉 Prediction completed successfully!")
        
        return render_template('prediction.html',
                             symbol=symbol,
                             historical_chart_data=historical_chart_data,
                             prediction_chart_data=prediction_chart_data,
                             historical_stats=historical_stats,
                             prediction_stats=prediction_stats,
                             current_price=current_price,
                             predicted_price=predicted_price,
                             change_percent=change_percent)
        
    except Exception as e:
        print(f"💥 Critical error in prediction: {str(e)}")
        traceback.print_exc()
        flash(f'Prediction failed: {str(e)}. Please try again.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/history')
@login_required
def prediction_history():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
        .order_by(PredictionHistory.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    total_predictions = current_user.get_prediction_count()
    all_predictions = PredictionHistory.query.filter_by(user_id=current_user.id).all()
    
    avg_change = 0
    bullish_count = 0
    bearish_count = 0
    
    if all_predictions:
        avg_change = sum(p.change_percent for p in all_predictions) / len(all_predictions)
        bullish_count = sum(1 for p in all_predictions if p.change_percent > 0)
        bearish_count = len(all_predictions) - bullish_count
    
    stats = {
        'total_predictions': total_predictions,
        'avg_change_percent': avg_change,
        'bullish_predictions': bullish_count,
        'bearish_predictions': bearish_count
    }
    
    return render_template('history.html', predictions=predictions, stats=stats)

@app.route('/history/<int:prediction_id>')
@login_required
def view_prediction(prediction_id):
    prediction = PredictionHistory.query.filter_by(id=prediction_id, user_id=current_user.id).first_or_404()
    
    # Use the same prediction.html template but with historical data
    return render_template('prediction.html',
                         symbol=prediction.symbol,
                         historical_chart_data=prediction.get_historical_chart_data(),
                         prediction_chart_data=prediction.get_prediction_chart_data(),
                         historical_stats=prediction.get_historical_stats(),
                         prediction_stats=prediction.get_prediction_stats(),
                         current_price=prediction.current_price,
                         predicted_price=prediction.predicted_price,
                         change_percent=prediction.change_percent,
                         is_historical=True,
                         prediction_date=prediction.created_at)

@app.route('/history/delete/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    prediction = PredictionHistory.query.filter_by(id=prediction_id, user_id=current_user.id).first_or_404()
    
    try:
        symbol = prediction.symbol
        db.session.delete(prediction)
        db.session.commit()
        flash(f'Prediction for {symbol} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting prediction.', 'error')
    
    return redirect(url_for('prediction_history'))

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    try:
        # Get form data
        current_password = request.form.get('current_password', '').strip()
        new_password = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validate input
        if not current_password or not new_password or not confirm_password:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        # Check if new passwords match
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'New passwords do not match'
            }), 400
        
        # Check minimum password length
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'message': 'New password must be at least 6 characters long'
            }), 400
        
        # Verify current password
        if not current_user.check_password(current_password):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 400
        
        # Check if new password is different from current
        if current_user.check_password(new_password):
            return jsonify({
                'success': False,
                'message': 'New password must be different from current password'
            }), 400
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        print(f"Password changed successfully for user: {current_user.username}")
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error changing password: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while changing password. Please try again.'
        }), 500

@app.route('/auth/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account permanently - FIXED VERSION"""
    try:
        # Get user information BEFORE any operations
        user_id = current_user.id
        username = current_user.username
        full_name = current_user.get_full_name()
        
        print(f"🗑️ Starting account deletion for user: {username} (ID: {user_id})")
        
        # Query the user from database to get a fresh instance
        user_to_delete = User.query.get(user_id)
        if not user_to_delete:
            raise ValueError("User not found in database")
        
        # Delete all associated prediction history manually (ensure cascade works)
        predictions_deleted = PredictionHistory.query.filter_by(user_id=user_id).delete()
        print(f"🗑️ Deleted {predictions_deleted} predictions for user {username}")
        
        # Delete the user account
        db.session.delete(user_to_delete)
        
        # Commit the transaction before logging out
        db.session.commit()
        print(f"✅ Successfully deleted account from database for user: {username}")
        
        # Now logout the user (after successful deletion)
        logout_user()
        print(f"✅ User {username} logged out successfully")
        
        # Return JSON response for AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': f'Account for {full_name} ({username}) has been permanently deleted.',
                'redirect': url_for('index')
            })
        else:
            # Handle regular form submission
            flash(f'Account {username} has been permanently deleted.', 'info')
            return redirect(url_for('index'))
        
    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        print(f"❌ Error deleting account: {error_msg}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        
        # Return error response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'message': f'Failed to delete account: {error_msg}'
            }), 500
        else:
            flash('Error deleting account. Please try again.', 'error')
            return redirect(url_for('profile'))

@app.route('/profile')
@login_required
def profile():
    user = current_user
    recent_predictions = user.get_recent_predictions(limit=10)
    total_predictions = user.get_prediction_count()
    
    stats = {
        'total_predictions': total_predictions,
        'member_since': user.created_at.strftime('%B %Y'),
        'last_login': user.last_login.strftime('%B %d, %Y at %I:%M %p') if user.last_login else 'Never',
        'account_age_days': (datetime.utcnow() - user.created_at).days
    }
    
    return render_template('auth/profile.html', user=user, recent_predictions=recent_predictions, stats=stats)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully")

if __name__ == '__main__':
    print("🚀 Starting AI Stock Predictor with Authentication...")
    print(f"📊 Sequence Length: {app.config['SEQUENCE_LENGTH']}")
    print(f"🔮 Prediction Days: {app.config['PREDICTION_DAYS']}")
    app.run(debug=True, host='0.0.0.0', port=5000)