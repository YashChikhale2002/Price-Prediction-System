import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def prepare_data(stock_data, sequence_length=60, target_column='Close'):
    """
    Prepare stock data for LSTM training with robust error handling
    
    Args:
        stock_data (pd.DataFrame): Raw stock data
        sequence_length (int): Length of input sequences
        target_column (str): Column to predict
    
    Returns:
        tuple: (X_train, y_train, X_test, scaler, last_sequence)
    """
    try:
        print(f"🔄 Preparing data with sequence length: {sequence_length}")
        
        # Validate input data
        if stock_data is None or stock_data.empty:
            raise ValueError("Stock data is empty or None")
        
        if target_column not in stock_data.columns:
            raise ValueError(f"Target column '{target_column}' not found in data")
        
        # Remove any NaN values
        stock_data = stock_data.dropna()
        
        if len(stock_data) < sequence_length + 10:  # Need extra data for training
            raise ValueError(f"Insufficient data: {len(stock_data)} rows, need at least {sequence_length + 10}")
        
        # Extract the target column
        prices = stock_data[target_column].values.reshape(-1, 1)
        print(f"📊 Extracted {len(prices)} price points")
        
        # Validate price data
        if np.any(np.isnan(prices)) or np.any(np.isinf(prices)):
            print("⚠️ Found NaN or Inf values in prices, cleaning...")
            prices = np.nan_to_num(prices, nan=0.0, posinf=np.finfo(np.float64).max, neginf=0.0)
        
        # Scale the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(prices)
        print(f"✅ Data scaled to range [0, 1]")
        
        # Create sequences
        X, y = create_sequences(scaled_data, sequence_length)
        print(f"📈 Created {len(X)} sequences of length {sequence_length}")
        
        if len(X) == 0:
            raise ValueError("No sequences created - data too short")
        
        # Split into train and test sets (80/20 split)
        train_size = max(1, int(len(X) * 0.8))  # Ensure at least 1 training sample
        
        X_train = X[:train_size]
        y_train = y[:train_size]
        X_test = X[train_size:] if train_size < len(X) else np.array([])
        
        print(f"🎯 Training set: {len(X_train)} samples")
        print(f"🎯 Test set: {len(X_test)} samples")
        
        # Get the last sequence for future predictions
        last_sequence = scaled_data[-sequence_length:].flatten()
        print(f"🔮 Last sequence prepared for future predictions: {len(last_sequence)} points")
        
        # Validate outputs
        if len(X_train) == 0:
            raise ValueError("No training data created")
        
        print("✅ Data preparation completed successfully")
        return X_train, y_train, X_test, scaler, last_sequence
        
    except Exception as e:
        print(f"❌ Error in data preparation: {str(e)}")
        raise

def create_sequences(data, sequence_length):
    """
    Create input sequences and corresponding targets with validation
    
    Args:
        data (np.array): Scaled price data
        sequence_length (int): Length of input sequences
    
    Returns:
        tuple: (X, y) - sequences and targets
    """
    try:
        print(f"🔄 Creating sequences from {len(data)} data points")
        
        if len(data) <= sequence_length:
            print(f"⚠️ Data length ({len(data)}) is not sufficient for sequence length ({sequence_length})")
            return np.array([]), np.array([])
        
        X, y = [], []
        
        for i in range(sequence_length, len(data)):
            sequence = data[i-sequence_length:i, 0]
            target = data[i, 0]
            
            # Validate sequence
            if not np.any(np.isnan(sequence)) and not np.any(np.isinf(sequence)):
                X.append(sequence)
                y.append(target)
        
        if len(X) == 0:
            print("❌ No valid sequences created")
            return np.array([]), np.array([])
        
        X = np.array(X)
        y = np.array(y)
        
        # Reshape X to be 3D for LSTM [samples, time steps, features]
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        print(f"✅ Created {len(X)} sequences with shape {X.shape}")
        return X, y
        
    except Exception as e:
        print(f"❌ Error creating sequences: {str(e)}")
        raise

def validate_and_clean_data(stock_data):
    """
    Validate and clean stock data
    
    Args:
        stock_data (pd.DataFrame): Raw stock data
    
    Returns:
        pd.DataFrame: Cleaned stock data
    """
    try:
        print("🧹 Cleaning and validating stock data...")
        
        if stock_data is None or stock_data.empty:
            raise ValueError("Stock data is empty")
        
        # Remove rows with NaN values in essential columns
        essential_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        available_columns = [col for col in essential_columns if col in stock_data.columns]
        
        original_length = len(stock_data)
        stock_data = stock_data.dropna(subset=available_columns)
        
        if len(stock_data) < original_length:
            print(f"⚠️ Removed {original_length - len(stock_data)} rows with NaN values")
        
        # Validate price data (prices should be positive)
        for col in ['Open', 'High', 'Low', 'Close']:
            if col in stock_data.columns:
                stock_data = stock_data[stock_data[col] > 0]
        
        # Validate volume (should be non-negative)
        if 'Volume' in stock_data.columns:
            stock_data = stock_data[stock_data['Volume'] >= 0]
        
        # Sort by date
        stock_data = stock_data.sort_index()
        
        print(f"✅ Data cleaned: {len(stock_data)} valid rows remaining")
        return stock_data
        
    except Exception as e:
        print(f"❌ Error cleaning data: {str(e)}")
        raise

def calculate_technical_indicators(stock_data):
    """
    Calculate technical indicators for the stock data
    
    Args:
        stock_data (pd.DataFrame): Stock data with OHLCV columns
    
    Returns:
        pd.DataFrame: Stock data with technical indicators added
    """
    try:
        print("📊 Calculating technical indicators...")
        df = stock_data.copy()
        
        # Moving averages
        if 'Close' in df.columns:
            df['MA_10'] = df['Close'].rolling(window=10, min_periods=1).mean()
            df['MA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()
            df['MA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
            
            # RSI (Relative Strength Index)
            df['RSI'] = calculate_rsi(df['Close'])
            
            # MACD
            df['MACD'], df['MACD_Signal'] = calculate_macd(df['Close'])
            
            # Bollinger Bands
            df['BB_Upper'], df['BB_Lower'] = calculate_bollinger_bands(df['Close'])
            
            print("✅ Technical indicators calculated")
        
        return df
        
    except Exception as e:
        print(f"❌ Error calculating technical indicators: {str(e)}")
        return stock_data  # Return original data if indicators fail

def calculate_rsi(prices, window=14):
    """Calculate RSI indicator with error handling"""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
        rs = gain / loss.replace(0, np.finfo(float).eps)  # Avoid division by zero
        return 100 - (100 / (1 + rs))
    except:
        return pd.Series(50, index=prices.index)  # Return neutral RSI on error

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD indicator with error handling"""
    try:
        exp1 = prices.ewm(span=fast, min_periods=1).mean()
        exp2 = prices.ewm(span=slow, min_periods=1).mean()
        macd = exp1 - exp2
        macd_signal = macd.ewm(span=signal, min_periods=1).mean()
        return macd, macd_signal
    except:
        zeros = pd.Series(0, index=prices.index)
        return zeros, zeros

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculate Bollinger Bands with error handling"""
    try:
        ma = prices.rolling(window=window, min_periods=1).mean()
        std = prices.rolling(window=window, min_periods=1).std()
        upper_band = ma + (std * num_std)
        lower_band = ma - (std * num_std)
        return upper_band, lower_band
    except:
        return prices, prices  # Return price series on error