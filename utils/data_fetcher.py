import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol, period='1y'):
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
        period (str): Period to fetch data ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    
    Returns:
        pandas.DataFrame: Stock data with OHLCV columns
    """
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Fetch historical data
        stock_data = ticker.history(period=period)
        
        if stock_data.empty:
            print(f"No data found for symbol: {symbol}")
            return None
        
        # Remove timezone info for easier handling
        stock_data.index = stock_data.index.tz_localize(None)
        
        return stock_data
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

def get_stock_info(symbol):
    """
    Get basic information about a stock
    
    Args:
        symbol (str): Stock symbol
    
    Returns:
        dict: Stock information
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'symbol': symbol,
            'company_name': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'current_price': info.get('regularMarketPrice', 'N/A')
        }
    
    except Exception as e:
        print(f"Error fetching info for {symbol}: {str(e)}")
        return None

def validate_symbol(symbol):
    """
    Validate if a stock symbol exists
    
    Args:
        symbol (str): Stock symbol to validate
    
    Returns:
        bool: True if symbol exists, False otherwise
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        return not data.empty
    
    except:
        return False