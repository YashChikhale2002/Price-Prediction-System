# Stock Market Price Prediction System

## 🚀 Project Overview

The **Stock Market Price Prediction System** is an advanced AI-powered web application that leverages LSTM neural networks to predict stock market prices. Built with modern web technologies, it provides professional-grade trading analytics with real-time data integration and interactive visualizations.

### ✨ Key Features

- 🧠 **AI-Powered Predictions** - Advanced LSTM neural networks for accurate price forecasting
- 📊 **Real-time Market Data** - Live stock data integration via Yahoo Finance API
- 📈 **Interactive Charts** - Professional Chart.js visualizations with responsive design
- 👥 **User Management** - Secure authentication and personalized dashboards
- 📱 **Mobile Responsive** - Optimized for all device sizes with modern UI/UX
- 🔒 **Secure Authentication** - Flask-Login with password hashing and session management
- 📋 **Prediction History** - Complete tracking and management of user predictions
- 🎨 **Modern UI** - Glassmorphism design with Tailwind CSS and custom animations

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Lightweight web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **TensorFlow/Keras** - Machine learning framework
- **NumPy & Pandas** - Data processing and analysis
- **yfinance** - Yahoo Finance API integration

### Frontend
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization
- **Alpine.js** - Lightweight reactivity
- **Font Awesome** - Icon library

### Database
- **SQLite3** - Lightweight relational database
- **Database Schema** - Users, Predictions, and Sessions

### Development Tools
- **Flask-WTF** - Form handling and CSRF protection
- **Werkzeug** - WSGI utilities and security
- **Jinja2** - Template engine

## 📁 Project Structure

```
Stock-market-price-prediction/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── forms.py                        # WTForms form definitions
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── 
├── models/
│   ├── __init__.py
│   ├── database.py                 # Database models (User, PredictionHistory)
│   └── lstm_model.py              # LSTM neural network implementation
├── 
├── routes/
│   ├── __init__.py
│   ├── auth.py                     # Authentication routes (login, register, logout)
│   └── main.py                     # Main application routes (dashboard, predict, history)
├── 
├── utils/
│   ├── __init__.py
│   ├── data_fetcher.py            # Stock data fetching utilities
│   └── data_processor.py          # Data preprocessing for ML model
├── 
├── templates/
│   ├── base.html                   # Base template with navigation and footer
│   ├── index.html                  # Landing page
│   ├── dashboard.html              # User dashboard
│   ├── prediction.html             # Prediction results page
│   ├── history.html                # Prediction history page
│   └── auth/
│       ├── login.html              # Login page
│       ├── register.html           # Registration page
│       └── profile.html            # User profile page
├── 
├── static/
│   ├── css/
│   │   └── style.css              # Custom CSS styles
│   └── js/
│       └── main.js                # Custom JavaScript functionality
├── 
├── instance/
│   └── stock_predictor.db         # SQLite database file
├── 
├── saved_models/                   # Trained ML models storage
└── venv/                          # Python virtual environment
```

## 🚦 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/stock-market-price-prediction.git
cd stock-market-price-prediction
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///stock_predictor.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 5: Initialize Database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Step 6: Run Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📋 Requirements.txt

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.0
Werkzeug==2.3.7
tensorflow==2.13.0
numpy==1.24.3
pandas==2.0.3
yfinance==0.2.18
scikit-learn==1.3.0
Jinja2==3.1.2
MarkupSafe==2.1.3
click==8.1.7
itsdangerous==2.1.2
```

## 🗃️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Prediction History Table
```sql
CREATE TABLE prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    period VARCHAR(10) NOT NULL,
    current_price FLOAT NOT NULL,
    predicted_price FLOAT NOT NULL,
    change_percent FLOAT NOT NULL,
    historical_stats TEXT,
    prediction_stats TEXT,
    historical_chart_data TEXT,
    prediction_chart_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    model_accuracy FLOAT,
    training_epochs INTEGER DEFAULT 30,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🔧 Configuration

### App Configuration (config.py)
```python
class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stock_predictor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEQUENCE_LENGTH = 60
    PREDICTION_DAYS = 30
    WTF_CSRF_ENABLED = True
```

## 📊 Machine Learning Model

### LSTM Neural Network Architecture

```python
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=True),
    Dropout(0.2),
    LSTM(50),
    Dropout(0.2),
    Dense(1)
])
```

### Model Features
- **Input Sequence Length**: 60 days of historical data
- **Prediction Window**: 30 days future forecast
- **Architecture**: 3-layer LSTM with dropout regularization
- **Training**: Adam optimizer with MSE loss function
- **Data Preprocessing**: MinMax scaling for normalization

## 🎨 Frontend Features

### UI/UX Design
- **Glassmorphism Effects** - Modern translucent design elements
- **Responsive Layout** - Mobile-first design approach
- **Interactive Charts** - Real-time data visualization
- **Dark Theme** - Professional dark mode interface
- **Smooth Animations** - CSS3 and JavaScript animations
- **Accessibility** - WCAG 2.1 compliant design

### JavaScript Features
- **Real-time Form Validation** - Client-side input validation
- **Auto-save Functionality** - Form data persistence
- **Loading States** - Visual feedback during processing
- **Notification System** - Toast notifications for user feedback
- **Keyboard Shortcuts** - Enhanced user productivity

## 🔐 Security Features

### Authentication & Authorization
- **Password Hashing** - Werkzeug secure password hashing
- **Session Management** - Flask-Login session handling
- **CSRF Protection** - WTF-CSRF form protection
- **Input Validation** - Server and client-side validation
- **SQL Injection Prevention** - SQLAlchemy ORM protection

### Data Security
- **Secure Headers** - Security headers implementation
- **Session Security** - Secure cookie configuration
- **Data Sanitization** - XSS prevention measures

## 📈 API Endpoints

### Authentication Routes
```
GET  /                     # Landing page
GET  /login                # Login page
POST /login                # Process login
GET  /register             # Registration page
POST /register             # Process registration
GET  /logout               # User logout
```

### Application Routes
```
GET  /dashboard            # User dashboard
POST /predict              # Generate stock prediction
GET  /history              # View prediction history
GET  /history/<id>         # View specific prediction
POST /history/delete/<id>  # Delete prediction
GET  /profile              # User profile page
POST /change-password      # Change user password
```

### API Routes
```
GET  /api/predictions      # Get user predictions (JSON)
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Stock symbol validation
- [ ] Prediction generation
- [ ] Chart rendering
- [ ] Prediction history management
- [ ] Password change functionality
- [ ] Mobile responsiveness
- [ ] Cross-browser compatibility

### Test User Accounts
```
Username: testuser
Email: test@example.com
Password: testpass123
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=production-secret-key
   ```

2. **Database Migration**
   ```bash
   flask db upgrade
   ```

3. **Static File Serving**
   - Configure web server (Nginx/Apache) for static files
   - Use CDN for external libraries

4. **WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Solution: Initialize database
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

2. **Module Import Error**
   ```bash
   # Solution: Activate virtual environment
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Stock Data Fetch Error**
   ```
   # Check internet connection and Yahoo Finance API availability
   # Verify stock symbol exists and is valid
   ```

4. **Chart Rendering Issues**
   ```javascript
   // Check browser console for JavaScript errors
   // Ensure Chart.js library is loaded properly
   ```

## 📝 Development Notes

### Code Style
- **PEP 8** compliance for Python code
- **ES6+** standards for JavaScript
- **BEM methodology** for CSS naming
- **Semantic HTML5** markup

### Git Workflow
```bash
# Feature development
git checkout -b feature/new-feature
git add .
git commit -m "Add: new feature description"
git push origin feature/new-feature

# Create pull request for review
```

## 🔄 Future Enhancements

### Planned Features
- [ ] **Multi-timeframe Analysis** - 1h, 4h, daily predictions
- [ ] **Portfolio Management** - Track multiple stocks
- [ ] **Email Notifications** - Price alerts and predictions
- [ ] **Advanced Charts** - Candlestick and technical indicators
- [ ] **Mobile App** - React Native mobile application
- [ ] **API Integration** - RESTful API for third-party access
- [ ] **Real-time Updates** - WebSocket live data feeds
- [ ] **Social Features** - Share predictions and insights

### Technical Improvements
- [ ] **Model Optimization** - Hyperparameter tuning
- [ ] **Caching Layer** - Redis for improved performance
- [ ] **Background Tasks** - Celery for async processing
- [ ] **Monitoring** - Application performance monitoring
- [ ] **Testing Suite** - Comprehensive unit and integration tests

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Make changes and test thoroughly
4. Submit pull request with detailed description

### Contribution Guidelines
- Follow existing code style and structure
- Add appropriate comments and documentation
- Test all functionality before submitting
- Update README if adding new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

### Technical Support
- **Issues**: Create GitHub issue with detailed description
- **Documentation**: Refer to inline code comments
- **Community**: Join project discussions

### Project Maintainer
- **Developer**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [@your-username]

## 🙏 Acknowledgments

- **Yahoo Finance** - Stock data API
- **TensorFlow** - Machine learning framework
- **Flask Community** - Web framework support
- **Chart.js** - Data visualization library
- **Tailwind CSS** - Styling framework

---

## 📊 Project Statistics

- **Total Lines of Code**: ~5,000+
- **Templates**: 8 HTML files
- **Routes**: 15+ endpoints
- **Database Tables**: 2 main tables
- **JavaScript Functions**: 50+ utility functions
- **CSS Classes**: 200+ custom styles

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅

---

*This README provides comprehensive documentation for successful project handover and future development.*