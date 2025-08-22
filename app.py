from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from models.lstm_model import StockPredictor
from utils.data_fetcher import fetch_stock_data
from utils.data_processor import prepare_data
from config import Config
import pandas as pd
import traceback

app = Flask(__name__)
app.config.from_object(Config)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        symbol = request.form.get('symbol', '').upper().strip()
        period = request.form.get('period', '1y')
        
        print(f"🎯 Starting prediction for {symbol} with {period} period")
        
        # Validate input
        if not symbol:
            return jsonify({'error': 'Please provide a stock symbol'}), 400
        
        if len(symbol) > 10:
            return jsonify({'error': 'Invalid stock symbol'}), 400
        
        # Fetch stock data
        print(f"📡 Fetching stock data for {symbol}...")
        stock_data = fetch_stock_data(symbol, period)
        
        if stock_data is None or stock_data.empty:
            print(f"❌ No data found for {symbol}")
            return jsonify({'error': f'Could not fetch data for symbol {symbol}. Please check if the symbol exists.'}), 400
        
        print(f"✅ Fetched {len(stock_data)} data points for {symbol}")
        
        # Validate minimum data requirement
        if len(stock_data) < app.config['SEQUENCE_LENGTH']:
            return jsonify({'error': f'Insufficient data for {symbol}. Need at least {app.config["SEQUENCE_LENGTH"]} days of data.'}), 400
        
        # Prepare data for training
        print("🔄 Preparing data for LSTM training...")
        try:
            X_train, y_train, X_test, scaler, last_sequence = prepare_data(
                stock_data, 
                app.config['SEQUENCE_LENGTH']
            )
            print(f"✅ Data prepared - Training: {len(X_train)}, Test: {len(X_test)}")
        except Exception as e:
            print(f"❌ Error preparing data: {str(e)}")
            return jsonify({'error': 'Error processing stock data. Please try again.'}), 500
        
        # Create and train model
        print("🧠 Creating and training LSTM model...")
        try:
            predictor = StockPredictor(
                sequence_length=app.config['SEQUENCE_LENGTH'],
                n_features=1
            )
            
            # Train the model with reduced epochs for faster response
            print("🏋️ Training neural network...")
            history = predictor.train(X_train, y_train, epochs=30, batch_size=32, validation_split=0.1)
            print("✅ Model training completed")
        except Exception as e:
            print(f"❌ Error training model: {str(e)}")
            return jsonify({'error': 'Error training prediction model. Please try again.'}), 500
        
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
                days=app.config['PREDICTION_DAYS']
            )
            print(f"✅ Generated {len(future_predictions)} future predictions")
            
            # Validate predictions
            if len(future_predictions) == 0:
                raise ValueError("No future predictions generated")
            
        except Exception as e:
            print(f"❌ Error generating predictions: {str(e)}")
            return jsonify({'error': 'Error generating predictions. Please try again.'}), 500
        
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
            return jsonify({'error': 'Error preparing chart data. Please try again.'}), 500
    
    except Exception as e:
        print(f"💥 Critical error in prediction: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': f'Prediction failed: {str(e)}. Please try again.'}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"💥 Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error. Please try again later.'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Stock Predictor Flask Application...")
    print(f"📊 Sequence Length: {app.config['SEQUENCE_LENGTH']}")
    print(f"🔮 Prediction Days: {app.config['PREDICTION_DAYS']}")
    app.run(debug=True, host='0.0.0.0', port=5000)