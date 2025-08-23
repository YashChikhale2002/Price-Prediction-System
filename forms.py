# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models.database import User
import re

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username or Email', validators=[
        DataRequired(message='Username or email is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ], render_kw={'placeholder': 'Enter your username or email', 'class': 'form-input'})
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ], render_kw={'placeholder': 'Enter your password', 'class': 'form-input'})
    
    remember_me = BooleanField('Remember Me', render_kw={'class': 'form-checkbox'})
    
    submit = SubmitField('Sign In', render_kw={'class': 'btn-primary'})

class RegistrationForm(FlaskForm):
    """Registration form"""
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=50, message='First name must be between 2 and 50 characters')
    ], render_kw={'placeholder': 'Enter your first name', 'class': 'form-input'})
    
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=50, message='Last name must be between 2 and 50 characters')
    ], render_kw={'placeholder': 'Enter your last name', 'class': 'form-input'})
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ], render_kw={'placeholder': 'Choose a username', 'class': 'form-input'})
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be less than 120 characters')
    ], render_kw={'placeholder': 'Enter your email address', 'class': 'form-input'})
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, max=128, message='Password must be between 6 and 128 characters')
    ], render_kw={'placeholder': 'Create a password', 'class': 'form-input'})
    
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ], render_kw={'placeholder': 'Confirm your password', 'class': 'form-input'})
    
    submit = SubmitField('Create Account', render_kw={'class': 'btn-primary'})
    
    def validate_username(self, username):
        """Check if username is already taken"""
        # Check for valid username format (alphanumeric and underscore only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username.data):
            raise ValidationError('Username can only contain letters, numbers, and underscores')
        
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email or try logging in.')
    
    def validate_password(self, password):
        """Validate password strength"""
        password_value = password.data
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password_value):
            raise ValidationError('Password must contain at least one uppercase letter')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password_value):
            raise ValidationError('Password must contain at least one lowercase letter')
        
        # Check for at least one digit
        if not re.search(r'\d', password_value):
            raise ValidationError('Password must contain at least one number')

class StockPredictionForm(FlaskForm):
    """Enhanced stock prediction form"""
    symbol = StringField('Stock Symbol', validators=[
        DataRequired(message='Stock symbol is required'),
        Length(min=1, max=10, message='Stock symbol must be between 1 and 10 characters')
    ], render_kw={'placeholder': 'e.g., AAPL, GOOGL, TSLA', 'class': 'form-input'})
    
    period = SelectField('Analysis Period', choices=[
        ('6mo', '6 Months'),
        ('1y', '1 Year'),
        ('2y', '2 Years'),
        ('5y', '5 Years')
    ], default='1y', render_kw={'class': 'form-select'})
    
    submit = SubmitField('Generate AI Prediction', render_kw={'class': 'btn-primary'})
    
    def validate_symbol(self, symbol):
        """Validate stock symbol format"""
        symbol_value = symbol.data.upper().strip()
        
        # Check for valid symbol format (letters only)
        if not re.match(r'^[A-Z]+$', symbol_value):
            raise ValidationError('Stock symbol can only contain letters')
        
        # Update the field with cleaned value
        symbol.data = symbol_value