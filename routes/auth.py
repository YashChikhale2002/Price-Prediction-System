# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models.database import db, User
from forms import LoginForm, RegistrationForm
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        username_or_email = form.username.data.lower().strip()
        password = form.password.data
        remember = form.remember_me.data
        
        # Try to find user by username or email
        user = None
        if '@' in username_or_email:
            # It's an email
            user = User.query.filter_by(email=username_or_email).first()
        else:
            # It's a username
            user = User.query.filter_by(username=username_or_email).first()
        
        # Check credentials
        if user and user.check_password(password) and user.is_active:
            # Update last login time
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Log user in
            login_user(user, remember=remember)
            
            # Flash success message
            flash(f'Welcome back, {user.first_name}!', 'success')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username/email or password. Please try again.', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    # Redirect if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Create new user
            user = User(
                username=form.username.data.lower().strip(),
                email=form.email.data.lower().strip(),
                first_name=form.first_name.data.strip().title(),
                last_name=form.last_name.data.strip().title(),
                created_at=datetime.utcnow()
            )
            user.set_password(form.password.data)
            
            # Add to database
            db.session.add(user)
            db.session.commit()
            
            # Flash success message
            flash(f'Registration successful! Welcome to AI Stock Predictor, {user.first_name}!', 'success')
            
            # Log user in automatically
            login_user(user, remember=True)
            
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            print(f"Registration error: {str(e)}")
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    username = current_user.username
    logout_user()
    flash(f'You have been logged out successfully. See you next time!', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = current_user
    recent_predictions = user.get_recent_predictions(limit=10)
    
    # Calculate user statistics
    total_predictions = user.get_prediction_count()
    
    # Calculate average accuracy or other stats if needed
    stats = {
        'total_predictions': total_predictions,
        'member_since': user.created_at.strftime('%B %Y'),
        'last_login': user.last_login.strftime('%B %d, %Y at %I:%M %p') if user.last_login else 'Never',
        'account_age_days': (datetime.utcnow() - user.created_at).days
    }
    
    return render_template('auth/profile.html', 
                         user=user, 
                         recent_predictions=recent_predictions,
                         stats=stats)

@auth_bp.route('/delete-account', methods=['POST'])
@login_required
def delete_account():
    """Delete user account (with confirmation)"""
    try:
        user = current_user
        username = user.username
        
        # Delete user and all associated predictions (cascade)
        db.session.delete(user)
        db.session.commit()
        
        # Logout user
        logout_user()
        
        flash(f'Account {username} has been deleted successfully.', 'info')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        db.session.rollback()
        flash('Error deleting account. Please try again.', 'error')
        print(f"Account deletion error: {str(e)}")
        return redirect(url_for('auth.profile'))