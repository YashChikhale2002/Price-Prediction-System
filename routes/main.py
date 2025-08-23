# routes/main.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db, PredictionHistory
from models.lstm_model import StockPredictor
from utils.data_fetcher import fetch_stock_data
from utils.data_processor import prepare_data
from forms import StockPredictionForm
from config import Config
import pandas as pd
import numpy as np
import traceback
from datetime import datetime

main_bp = Blueprint('main', __name__)

def create_chart_data(dates, prices, name):
    """Create chart data structure for frontend with robust error handling"""
    try:
        print(f"🔄 Creating chart data for {name}")
        print(f"   Input - Dates type: {type(dates)}, length: {len(dates) if hasattr(dates, '__len__') else 'N/A'}")
        print(f"   Input - Prices type: {type(prices)}, length: {len(prices) if hasattr(prices, '__len__') else 'N/A'}")
        
        # Validate inputs
        if dates is None or prices is None:
            raise ValueError(f"No data available for {name} - None values")
        
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
        
        # Validate data length
        if len(dates_list) == 0 or len(prices_list) == 0:
            raise ValueError(f"Empty data arrays for {name}")
        
        if len(dates_list) != len(prices_list):
            min_length = min(len(dates_list), len(prices_list))
            print(f"⚠️ Mismatched lengths for {name}, trimming to {min_length}")
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
        
        # Create chart data structure
        chart_data = {
            'labels': formatted_dates,
            'prices': formatted_prices,
            'name': name,
            'min_price': float(min(formatted_prices)) if formatted_prices else 0.0,
            'max_price': float(max(formatted_prices)) if formatted_prices else 0.0,
            'avg_price': float(sum(formatted_prices) / len(formatted_prices)) if formatted_prices else 0.0
        }
        
        print(f"✅ Chart data created for {name}:")
        print(f"   📊 {len(formatted_prices)} data points")
        print(f"   💰 Price range: ${chart_data['min_price']:.2f} - ${chart_data['max_price']:.2f}")
        print(f"   📈 Average: ${chart_data['avg_price']:.2f}")
        
        return chart_data
    
    except Exception as e:
        print(f"❌ Error creating chart data for {name}: {str(e)}")
        traceback.print_exc()
        
        # Return safe fallback data
        fallback_data = {
            'labels': ['2025-01-01', '2025-01-02', '2025-01-03'],
            'prices': [100.0, 102.0, 101.0],
            'name': f"{name} (Error)",
            'min_price': 100.0,
            'max_price': 102.0,
            'avg_price': 101.0
        }
        print(f"🔄 Using fallback data for {name}")
        return fallback_data

@main_bp.route('/')
def index():
    """Landing page - redirect based on authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with prediction form"""
    form = StockPredictionForm()
    
    # Get user's recent predictions
    recent_predictions = current_user.get_recent_predictions(limit=5)
    
    # Get user statistics
    total_predictions = current_user.get_prediction_count()
    
    return render_template('dashboard.html', 
                         form=form, 
                         recent_predictions=recent_predictions,
                         total_predictions=total_predictions)

@main_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    """Generate stock prediction (requires authentication)"""
    try:
        # Get form data
        symbol = request.form.get('symbol', '').upper().strip()
        period = request.form.get('period', '1y')
        
        print(f"🎯 Starting prediction for {symbol} with {period} period (User: {current_user.username})")
        
        # Validate input
        if not symbol:
            flash('Please provide a stock symbol', 'error')
            return redirect(url_for('main.dashboard'))
        
        if len(symbol) > 10:
            flash('Invalid stock symbol', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Fetch stock data
        print(f"📡 Fetching stock data for {symbol}...")
        stock_data = fetch_stock_data(symbol, period)
        
        if stock_data is None or stock_data.empty:
            print(f"❌ No data found for {symbol}")
            flash(f'Could not fetch data for symbol {symbol}. Please check if the symbol exists.', 'error')
            return redirect(url_for('main.dashboard'))
        
        print(f"✅ Fetched {len(stock_data)} data points for {symbol}")
        
        # Validate minimum data requirement
        if len(stock_data) < Config.SEQUENCE_LENGTH:
            flash(f'Insufficient data for {symbol}. Need at least {Config.SEQUENCE_LENGTH} days of data.', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Prepare data for training
        print("🔄 Preparing data for LSTM training...")
        try:
            X_train, y_train, X_test, scaler, last_sequence = prepare_data(
                stock_data, 
                Config.SEQUENCE_LENGTH
            )
            print(f"✅ Data prepared - Training: {len(X_train)}, Test: {len(X_test)}")
        except Exception as e:
            print(f"❌ Error preparing data: {str(e)}")
            flash('Error processing stock data. Please try again.', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Create and train model
        print("🧠 Creating and training LSTM model...")
        try:
            predictor = StockPredictor(
                sequence_length=Config.SEQUENCE_LENGTH,
                n_features=1
            )
            
            # Train the model with reduced epochs for faster response
            print("🏋️ Training neural network...")
            history = predictor.train(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1)
            print("✅ Model training completed")
        except Exception as e:
            print(f"❌ Error training model: {str(e)}")
            flash('Error training prediction model. Please try again.', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Make predictions
        print("🔮 Generating predictions...")
        try:
            # Test predictions (if we have test data)
            if len(X_test) > 0:
                test_predictions = predictor.predict(X_test, scaler)
                print(f"✅ Generated {len(test_predictions)} test predictions")
            else:
                test_predictions = np.array([])
                print("ℹ️ No test data available")
            
            # Future predictions
            future_predictions = predictor.predict_future(
                last_sequence, 
                scaler, 
                days=Config.PREDICTION_DAYS
            )
            print(f"✅ Generated {len(future_predictions)} future predictions")
            
            # Validate predictions
            if len(future_predictions) == 0:
                raise ValueError("No future predictions generated")
            
        except Exception as e:
            print(f"❌ Error generating predictions: {str(e)}")
            flash('Error generating predictions. Please try again.', 'error')
            return redirect(url_for('main.dashboard'))
        
        # Prepare data for visualization
        print("📊 Preparing visualization data...")
        try:
            # Historical data
            historical_prices = stock_data['Close'].values
            historical_dates = stock_data.index
            
            print(f"📈 Historical data: {len(historical_prices)} points")
            print(f"📅 Date range: {historical_dates[0]} to {historical_dates[-1]}")
            
            # Create future dates (business days only)
            last_date = stock_data.index[-1]
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=len(future_predictions),
                freq='B'  # Business days
            )
            
            print(f"🔮 Future predictions: {len(future_predictions)} points")
            print(f"📅 Prediction range: {future_dates[0]} to {future_dates[-1]}")
            
            # Create chart data with error handling
            historical_chart_data = create_chart_data(
                historical_dates, 
                historical_prices, 
                'Historical Prices'
            )
            
            prediction_chart_data = create_chart_data(
                future_dates, 
                future_predictions, 
                'AI Predictions'
            )
            
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
            
            print(f"💰 Current: ${current_price:.2f}")
            print(f"🔮 Predicted: ${predicted_price:.2f}")
            print(f"📊 Change: {change_percent:.2f}%")
            
            # Save prediction to database
            try:
                prediction_record = PredictionHistory(
                    user_id=current_user.id,
                    symbol=symbol,
                    period=period,
                    current_price=current_price,
                    predicted_price=predicted_price,
                    change_percent=change_percent,
                    training_epochs=30
                )
                
                # Set JSON data
                prediction_record.set_historical_stats(historical_stats)
                prediction_record.set_prediction_stats(prediction_stats)
                prediction_record.set_historical_chart_data(historical_chart_data)
                prediction_record.set_prediction_chart_data(prediction_chart_data)
                
                db.session.add(prediction_record)
                db.session.commit()
                
                print("✅ Prediction saved to database")
                
            except Exception as e:
                print(f"⚠️ Warning: Could not save prediction to database: {str(e)}")
                db.session.rollback()
            
            print("🎉 Prediction completed successfully!")
            
            # Render template with all data
            return render_template(
                'prediction.html',
                symbol=symbol,
                historical_chart_data=historical_chart_data,
                prediction_chart_data=prediction_chart_data,
                historical_stats=historical_stats,
                prediction_stats=prediction_stats,
                current_price=current_price,
                predicted_price=predicted_price,
                change_percent=change_percent
            )
            
        except Exception as e:
            print(f"❌ Error preparing visualization: {str(e)}")
            traceback.print_exc()
            flash('Error preparing chart data. Please try again.', 'error')
            return redirect(url_for('main.dashboard'))
    
    except Exception as e:
        print(f"💥 Critical error in prediction: {str(e)}")
        traceback.print_exc()
        flash(f'Prediction failed: {str(e)}. Please try again.', 'error')
        return redirect(url_for('main.dashboard'))

@main_bp.route('/history')
@login_required
def prediction_history():
    """View all prediction history for current user"""
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of predictions per page
    
    # Get user's predictions with pagination
    predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
        .order_by(PredictionHistory.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # Calculate statistics
    total_predictions = current_user.get_prediction_count()
    
    # Calculate average change percent
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
        'bearish_predictions': bearish_count,
        'accuracy_rate': 0  # Could be calculated based on actual vs predicted if you track that
    }
    
    return render_template('history.html', 
                         predictions=predictions, 
                         stats=stats)

@main_bp.route('/history/<int:prediction_id>')
@login_required
def view_prediction(prediction_id):
    """View detailed prediction"""
    prediction = PredictionHistory.query.filter_by(
        id=prediction_id, 
        user_id=current_user.id
    ).first_or_404()
    
    return render_template('prediction_detail.html', 
                         prediction=prediction,
                         symbol=prediction.symbol,
                         historical_chart_data=prediction.get_historical_chart_data(),
                         prediction_chart_data=prediction.get_prediction_chart_data(),
                         historical_stats=prediction.get_historical_stats(),
                         prediction_stats=prediction.get_prediction_stats(),
                         current_price=prediction.current_price,
                         predicted_price=prediction.predicted_price,
                         change_percent=prediction.change_percent)

@main_bp.route('/history/delete/<int:prediction_id>', methods=['POST'])
@login_required
def delete_prediction(prediction_id):
    """Delete a prediction from history"""
    prediction = PredictionHistory.query.filter_by(
        id=prediction_id, 
        user_id=current_user.id
    ).first_or_404()
    
    try:
        symbol = prediction.symbol
        db.session.delete(prediction)
        db.session.commit()
        flash(f'Prediction for {symbol} deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting prediction.', 'error')
        print(f"Delete prediction error: {str(e)}")
    
    return redirect(url_for('main.prediction_history'))

@main_bp.route('/api/predictions')
@login_required
def api_predictions():
    """API endpoint for prediction data (for charts/widgets)"""
    predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
        .order_by(PredictionHistory.created_at.desc())\
        .limit(20).all()
    
    data = []
    for p in predictions:
        data.append({
            'id': p.id,
            'symbol': p.symbol,
            'current_price': p.current_price,
            'predicted_price': p.predicted_price,
            'change_percent': p.change_percent,
            'created_at': p.created_at.isoformat(),
            'sentiment': p.get_sentiment()['sentiment']
        })
    
    return jsonify(data)