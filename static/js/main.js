// Enhanced Professional JavaScript for Stock Prediction App

class StockPredictionApp {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupAnimations();
    }

    init() {
        // Initialize app components
        this.updateTime();
        this.setupFormValidation();
        this.setupStockButtons();
        this.setupChartInteractions();
        
        // Update time every second
        setInterval(() => this.updateTime(), 1000);
    }

    updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }

    setupEventListeners() {
        // Form submission handling
        const form = document.getElementById('predictionForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Stock button interactions
        document.querySelectorAll('.stock-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleStockButtonClick(e));
        });

        // Input field enhancements
        const symbolInput = document.getElementById('symbol');
        if (symbolInput) {
            symbolInput.addEventListener('input', (e) => this.handleSymbolInput(e));
            symbolInput.addEventListener('blur', (e) => this.validateSymbol(e.target.value));
            symbolInput.addEventListener('focus', (e) => this.handleInputFocus(e));
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Window resize handling for charts
        window.addEventListener('resize', this.debounce(() => {
            this.resizeCharts();
        }, 250));
    }

    handleFormSubmit(e) {
        const form = e.target;
        const loadingIndicator = document.getElementById('loadingIndicator');
        const submitBtn = document.getElementById('submitBtn');
        const buttonText = document.getElementById('buttonText');
        const formContent = form.querySelector('.space-y-6');

        // Validate form before submission
        if (!this.validateForm()) {
            e.preventDefault();
            return;
        }

        // Show enhanced loading state
        if (loadingIndicator && formContent) {
            this.showLoadingState(loadingIndicator, formContent, submitBtn, buttonText);
        }

        // Add progress simulation
        this.simulateProgress();
    }

    showLoadingState(loadingIndicator, formContent, submitBtn, buttonText) {
        // Hide form and show loading
        formContent.style.opacity = '0';
        formContent.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            formContent.classList.add('hidden');
            loadingIndicator.classList.remove('hidden');
            loadingIndicator.style.opacity = '0';
            loadingIndicator.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                loadingIndicator.style.opacity = '1';
                loadingIndicator.style.transform = 'translateY(0)';
            }, 100);
        }, 300);

        // Update button state
        if (submitBtn && buttonText) {
            submitBtn.disabled = true;
            submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
            buttonText.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Training Neural Network...';
        }
    }

    simulateProgress() {
        const progressSteps = [
            'Fetching market data...',
            'Preprocessing time series...',
            'Training LSTM model...',
            'Optimizing neural network...',
            'Generating predictions...',
            'Finalizing analysis...'
        ];

        let currentStep = 0;
        const buttonText = document.getElementById('buttonText');
        
        if (buttonText) {
            const interval = setInterval(() => {
                if (currentStep < progressSteps.length) {
                    buttonText.innerHTML = `<i class="fas fa-spinner fa-spin mr-2"></i>${progressSteps[currentStep]}`;
                    currentStep++;
                } else {
                    clearInterval(interval);
                }
            }, 2000);
        }
    }

    handleStockButtonClick(e) {
        const button = e.target.closest('.stock-btn');
        const symbol = button.getAttribute('data-symbol');
        const symbolInput = document.getElementById('symbol');
        
        if (symbolInput) {
            // Add selection animation
            this.animateStockSelection(button);
            
            // Update input value
            symbolInput.value = symbol;
            symbolInput.focus();
            
            // Trigger validation
            this.validateSymbol(symbol);
            
            // Auto-submit after a delay (optional)
            setTimeout(() => {
                if (symbolInput.value === symbol) {
                    this.highlightSubmitButton();
                }
            }, 500);
        }
    }

    animateStockSelection(button) {
        // Add ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'absolute inset-0 bg-white opacity-25 rounded-lg transform scale-0';
        ripple.style.transition = 'transform 0.3s ease';
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.style.transform = 'scale(1)';
        }, 10);
        
        setTimeout(() => {
            ripple.remove();
        }, 300);
        
        // Add selection feedback
        button.classList.add('animate-pulse', 'ring-2', 'ring-blue-400');
        setTimeout(() => {
            button.classList.remove('animate-pulse', 'ring-2', 'ring-blue-400');
        }, 1000);
    }

    handleSymbolInput(e) {
        const input = e.target;
        const originalValue = input.value;
        
        // Format input: uppercase, letters only, max 5 chars
        let formattedValue = originalValue.toUpperCase().replace(/[^A-Z]/g, '');
        if (formattedValue.length > 5) {
            formattedValue = formattedValue.substring(0, 5);
        }
        
        if (originalValue !== formattedValue) {
            input.value = formattedValue;
        }
        
        // Real-time validation feedback
        this.updateInputValidation(input, formattedValue);
    }

    updateInputValidation(input, value) {
        // Remove existing validation classes
        input.classList.remove('ring-green-500', 'ring-red-500', 'ring-yellow-500');
        
        if (value.length === 0) {
            // No input
            return;
        } else if (value.length >= 2 && value.length <= 5) {
            // Valid format
            input.classList.add('ring-2', 'ring-green-500');
            this.showValidationMessage('Symbol format looks good!', 'success');
        } else {
            // Invalid format
            input.classList.add('ring-2', 'ring-yellow-500');
            this.showValidationMessage('Enter 2-5 letters for stock symbol', 'warning');
        }
    }

    validateSymbol(symbol) {
        if (!symbol || symbol.length < 1) {
            this.showValidationMessage('Please enter a stock symbol', 'error');
            return false;
        }
        
        if (symbol.length < 2) {
            this.showValidationMessage('Symbol should be at least 2 characters', 'warning');
            return false;
        }
        
        if (symbol.length > 5) {
            this.showValidationMessage('Symbol should be 5 characters or less', 'error');
            return false;
        }
        
        // Check against common patterns
        if (!/^[A-Z]{2,5}$/.test(symbol)) {
            this.showValidationMessage('Use only letters (A-Z)', 'error');
            return false;
        }
        
        this.showValidationMessage('✓ Valid symbol format', 'success');
        return true;
    }

    showValidationMessage(message, type) {
        // Remove existing messages
        const existingMessage = document.querySelector('.validation-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = `validation-message mt-2 p-2 rounded-lg text-sm transition-all duration-300`;
        
        // Style based on type
        switch (type) {
            case 'success':
                messageDiv.className += ' bg-green-600/20 text-green-300 border border-green-600/30';
                break;
            case 'warning':
                messageDiv.className += ' bg-yellow-600/20 text-yellow-300 border border-yellow-600/30';
                break;
            case 'error':
                messageDiv.className += ' bg-red-600/20 text-red-300 border border-red-600/30';
                break;
        }
        
        messageDiv.textContent = message;
        
        // Insert after symbol input
        const symbolInput = document.getElementById('symbol');
        if (symbolInput && symbolInput.parentNode) {
            symbolInput.parentNode.appendChild(messageDiv);
            
            // Auto-remove after 4 seconds
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.style.opacity = '0';
                    messageDiv.style.transform = 'translateY(-10px)';
                    setTimeout(() => messageDiv.remove(), 300);
                }
            }, 4000);
        }
    }

    validateForm() {
        const symbolInput = document.getElementById('symbol');
        if (!symbolInput) return false;
        
        const symbol = symbolInput.value.trim();
        return this.validateSymbol(symbol);
    }

    handleInputFocus(e) {
        const input = e.target;
        input.classList.add('ring-2', 'ring-blue-500');
        
        // Add subtle glow effect
        input.style.boxShadow = '0 0 20px rgba(59, 130, 246, 0.3)';
        
        input.addEventListener('blur', () => {
            input.classList.remove('ring-2', 'ring-blue-500');
            input.style.boxShadow = '';
        }, { once: true });
    }

    highlightSubmitButton() {
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) {
            submitBtn.classList.add('animate-pulse', 'ring-4', 'ring-blue-400');
            setTimeout(() => {
                submitBtn.classList.remove('animate-pulse', 'ring-4', 'ring-blue-400');
            }, 2000);
        }
    }

    handleKeyboardShortcuts(e) {
        // Enter key to submit (when symbol input is focused and valid)
        if (e.key === 'Enter' && e.target.id === 'symbol') {
            const symbol = e.target.value.trim();
            if (this.validateSymbol(symbol)) {
                const form = document.getElementById('predictionForm');
                if (form) {
                    form.submit();
                }
            }
        }
        
        // Escape key to clear input
        if (e.key === 'Escape') {
            const symbolInput = document.getElementById('symbol');
            if (symbolInput && document.activeElement === symbolInput) {
                symbolInput.value = '';
                symbolInput.blur();
            }
        }
    }

    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe all elements with animation class
        document.querySelectorAll('.animate-on-load').forEach(el => {
            observer.observe(el);
        });
    }

    setupChartInteractions() {
        // Enhanced chart hover effects
        setTimeout(() => {
            const charts = document.querySelectorAll('[id$="Chart"]');
            charts.forEach(chart => {
                chart.addEventListener('mouseenter', this.handleChartHover.bind(this));
                chart.addEventListener('mouseleave', this.handleChartLeave.bind(this));
            });
        }, 1000);
    }

    handleChartHover(e) {
        e.target.style.transform = 'scale(1.01)';
        e.target.style.transition = 'transform 0.3s ease';
        e.target.style.zIndex = '10';
    }

    handleChartLeave(e) {
        e.target.style.transform = 'scale(1)';
        e.target.style.zIndex = '';
    }

    resizeCharts() {
        // Responsive chart resizing
        if (window.Plotly) {
            const charts = document.querySelectorAll('[id$="Chart"]');
            charts.forEach(chartElement => {
                if (chartElement.data) {
                    window.Plotly.Plots.resize(chartElement);
                }
            });
        }
    }

    // Utility function for debouncing
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Error handling and performance monitoring
class ErrorHandler {
    static init() {
        window.addEventListener('error', this.handleError.bind(this));
        window.addEventListener('unhandledrejection', this.handlePromiseRejection.bind(this));
    }

    static handleError(event) {
        console.error('JavaScript Error:', event.error);
        this.showUserFriendlyError('An unexpected error occurred. Please refresh the page and try again.');
    }

    static handlePromiseRejection(event) {
        console.error('Promise Rejection:', event.reason);
        this.showUserFriendlyError('A network error occurred. Please check your connection and try again.');
    }

    static showUserFriendlyError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-600/90 text-white px-6 py-4 rounded-lg shadow-lg z-50 transition-all duration-300 transform translate-x-full';
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-triangle mr-3"></i>
                <span>${message}</span>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(errorDiv);
        
        // Animate in
        setTimeout(() => {
            errorDiv.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            errorDiv.style.transform = 'translateX(full)';
            setTimeout(() => errorDiv.remove(), 300);
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StockPredictionApp();
    ErrorHandler.init();
    
    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            console.log(`Page loaded in ${loadTime}ms`);
        });
    }
});

// Service Worker registration for offline capability (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => console.log('SW registered'))
            .catch(error => console.log('SW registration failed'));
    });
}