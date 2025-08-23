/**
 * AI Stock Predictor - Enhanced Professional JavaScript
 * Modern, performance-optimized JavaScript for stock prediction app
 * Compatible with all templates and provides enhanced user experience
 */

// ========================================
// Core Application Class
// ========================================
class StockPredictorApp {
    constructor() {
        this.version = '2.0.0';
        this.config = {
            animationDuration: 300,
            debounceDelay: 250,
            notificationTimeout: 5000,
            chartUpdateInterval: 30000,
            maxRetries: 3
        };
        
        this.state = {
            isLoading: false,
            currentUser: null,
            notifications: new Map(),
            activeModals: new Set()
        };
        
        // Initialize app
        this.init();
    }

    init() {
        console.log(`🚀 AI Stock Predictor v${this.version} initializing...`);
        
        // Setup core functionality
        this.setupEventListeners();
        this.initializeTime();
        this.initializeAnimations();
        this.initializeFormEnhancements();
        this.initializeNotifications();
        this.initializeAccessibility();
        this.initializePerformanceOptimizations();
        
        // Page-specific initialization
        this.detectPageAndInitialize();
        
        console.log('✅ AI Stock Predictor initialized successfully');
    }

    // ========================================
    // Event Listeners Setup
    // ========================================
    setupEventListeners() {
        // DOM Content Loaded - ensure everything is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.onDOMReady());
        } else {
            this.onDOMReady();
        }

        // Window events
        window.addEventListener('resize', this.debounce(() => this.handleResize(), this.config.debounceDelay));
        window.addEventListener('scroll', this.throttle(() => this.handleScroll(), 16));
        window.addEventListener('beforeunload', () => this.handleBeforeUnload());
        
        // Error handling
        window.addEventListener('error', (e) => this.handleError(e));
        window.addEventListener('unhandledrejection', (e) => this.handlePromiseRejection(e));
        
        // Network status
        window.addEventListener('online', () => this.showNotification('Connection restored', 'success'));
        window.addEventListener('offline', () => this.showNotification('You are now offline', 'warning'));
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
        
        // Click outside handlers
        document.addEventListener('click', (e) => this.handleGlobalClick(e));
    }

    onDOMReady() {
        // Initialize mobile menu
        this.initializeMobileMenu();
        
        // Initialize form handling
        this.initializeFormHandling();
        
        // Initialize stock buttons
        this.initializeStockButtons();
        
        // Initialize charts if present
        this.initializeCharts();
        
        // Initialize modals
        this.initializeModals();
        
        // Initialize tooltips and popovers
        this.initializeTooltips();
        
        // Initialize table interactions
        this.initializeTableInteractions();
        
        // Show welcome message for new users
        this.showWelcomeMessage();
    }

    // ========================================
    // Page Detection and Initialization
    // ========================================
    detectPageAndInitialize() {
        const body = document.body;
        const currentPage = this.getCurrentPage();
        
        switch (currentPage) {
            case 'dashboard':
                this.initializeDashboard();
                break;
            case 'prediction':
                this.initializePredictionPage();
                break;
            case 'history':
                this.initializeHistoryPage();
                break;
            case 'profile':
                this.initializeProfilePage();
                break;
            case 'login':
            case 'register':
                this.initializeAuthPages();
                break;
            default:
                this.initializeGeneralPage();
        }
    }

    getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('dashboard')) return 'dashboard';
        if (path.includes('prediction') || path.includes('history')) {
            return path.includes('history') ? 'history' : 'prediction';
        }
        if (path.includes('profile')) return 'profile';
        if (path.includes('login')) return 'login';
        if (path.includes('register')) return 'register';
        return 'index';
    }

    // ========================================
    // Time Management
    // ========================================
    initializeTime() {
        this.updateTime();
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
        
        const timeElements = document.querySelectorAll('#current-time, #footer-time');
        timeElements.forEach(element => {
            if (element) element.textContent = timeString;
        });
    }

    // ========================================
    // Animation System
    // ========================================
    initializeAnimations() {
        // Setup Intersection Observer for scroll animations
        this.setupScrollAnimations();
        
        // Initialize page load animations
        this.animatePageLoad();
    }

    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        this.intersectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    element.classList.add('animate-fade-in');
                    
                    // Add stagger delay for multiple elements
                    const delay = Array.from(element.parentNode?.children || []).indexOf(element) * 100;
                    element.style.animationDelay = `${delay}ms`;
                    
                    this.intersectionObserver.unobserve(element);
                }
            });
        }, observerOptions);
        
        // Observe elements with animation classes
        document.querySelectorAll('.animate-on-load, .animate-on-scroll').forEach(el => {
            this.intersectionObserver.observe(el);
        });
    }

    animatePageLoad() {
        const animateElements = document.querySelectorAll('.animate-fade-in, .animate-slide-up');
        animateElements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s ease';
            
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }

    // ========================================
    // Mobile Menu Management
    // ========================================
    initializeMobileMenu() {
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        const menuIcon = mobileMenuButton?.querySelector('i');
        
        if (!mobileMenuButton || !mobileMenu) return;
        
        mobileMenuButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggleMobileMenu(mobileMenu, mobileMenuButton, menuIcon);
        });
        
        // Close menu on outside click
        document.addEventListener('click', (e) => {
            if (!mobileMenuButton.contains(e.target) && !mobileMenu.contains(e.target)) {
                this.closeMobileMenu(mobileMenu, mobileMenuButton, menuIcon);
            }
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mobileMenu.classList.contains('show')) {
                this.closeMobileMenu(mobileMenu, mobileMenuButton, menuIcon);
            }
        });
    }

    toggleMobileMenu(menu, button, icon) {
        const isOpen = menu.classList.contains('show');
        
        if (isOpen) {
            this.closeMobileMenu(menu, button, icon);
        } else {
            this.openMobileMenu(menu, button, icon);
        }
    }

    openMobileMenu(menu, button, icon) {
        menu.classList.add('show');
        button.setAttribute('aria-expanded', 'true');
        if (icon) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        }
    }

    closeMobileMenu(menu, button, icon) {
        menu.classList.remove('show');
        button.setAttribute('aria-expanded', 'false');
        if (icon) {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    }

    // ========================================
    // Form Enhancement System
    // ========================================
    initializeFormEnhancements() {
        // Enhanced form handling
        const enhancedForms = document.querySelectorAll('form[data-enhanced], #predictionForm');
        enhancedForms.forEach(form => this.enhanceForm(form));
        
        // Input validation
        this.initializeInputValidation();
        
        // Auto-save functionality
        this.initializeAutoSave();
    }

    enhanceForm(form) {
        if (!form) return;
        
        form.addEventListener('submit', (e) => this.handleFormSubmit(e, form));
        
        // Add loading states to submit buttons
        const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
        submitButtons.forEach(btn => this.enhanceSubmitButton(btn));
        
        // Enhance input fields
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => this.enhanceInput(input));
    }

    enhanceSubmitButton(button) {
        button.addEventListener('click', () => {
            const originalContent = button.innerHTML || button.value;
            button.dataset.originalContent = originalContent;
        });
    }

    enhanceInput(input) {
        // Add focus/blur effects
        input.addEventListener('focus', (e) => this.handleInputFocus(e));
        input.addEventListener('blur', (e) => this.handleInputBlur(e));
        
        // Real-time validation
        input.addEventListener('input', (e) => this.handleInputChange(e));
        
        // Special handling for stock symbol inputs
        if (input.name === 'symbol' || input.id === 'symbol') {
            this.enhanceSymbolInput(input);
        }
    }

    handleFormSubmit(e, form) {
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        
        // Show loading state
        if (submitBtn && !submitBtn.disabled) {
            this.setButtonLoading(submitBtn);
            
            // Show loading overlay for prediction forms
            if (form.id === 'predictionForm') {
                this.showLoadingOverlay();
            }
            
            // Fallback timeout
            setTimeout(() => {
                this.resetButtonLoading(submitBtn);
                this.hideLoadingOverlay();
            }, 30000);
        }
    }

    setButtonLoading(button) {
        const originalContent = button.dataset.originalContent || button.innerHTML || button.value;
        button.disabled = true;
        
        if (button.tagName === 'BUTTON') {
            button.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
        }
        
        button.classList.add('opacity-50', 'cursor-not-allowed');
    }

    resetButtonLoading(button) {
        const originalContent = button.dataset.originalContent;
        button.disabled = false;
        
        if (button.tagName === 'BUTTON' && originalContent) {
            button.innerHTML = originalContent;
        }
        
        button.classList.remove('opacity-50', 'cursor-not-allowed');
    }

    // ========================================
    // Stock Symbol Input Enhancement
    // ========================================
    enhanceSymbolInput(input) {
        input.addEventListener('input', (e) => {
            const value = e.target.value;
            const formatted = this.formatSymbolInput(value);
            
            if (value !== formatted) {
                e.target.value = formatted;
            }
            
            this.validateSymbolInput(e.target, formatted);
        });
    }

    formatSymbolInput(value) {
        return value.toUpperCase().replace(/[^A-Z]/g, '').substring(0, 5);
    }

    validateSymbolInput(input, value) {
        this.clearInputValidation(input);
        
        if (value.length === 0) return;
        
        if (value.length >= 2 && value.length <= 5) {
            this.setInputValidation(input, 'valid', '✓ Valid symbol format');
        } else if (value.length === 1) {
            this.setInputValidation(input, 'warning', 'Enter at least 2 characters');
        } else {
            this.setInputValidation(input, 'invalid', 'Symbol too long');
        }
    }

    setInputValidation(input, state, message) {
        input.classList.remove('ring-green-500', 'ring-yellow-500', 'ring-red-500');
        
        switch (state) {
            case 'valid':
                input.classList.add('ring-2', 'ring-green-500');
                break;
            case 'warning':
                input.classList.add('ring-2', 'ring-yellow-500');
                break;
            case 'invalid':
                input.classList.add('ring-2', 'ring-red-500');
                break;
        }
        
        this.showInputMessage(input, message, state);
    }

    clearInputValidation(input) {
        input.classList.remove('ring-2', 'ring-green-500', 'ring-yellow-500', 'ring-red-500');
        this.clearInputMessage(input);
    }

    showInputMessage(input, message, type) {
        this.clearInputMessage(input);
        
        const messageEl = document.createElement('div');
        messageEl.className = `input-validation-message mt-2 p-2 rounded-lg text-sm transition-all duration-300`;
        messageEl.setAttribute('role', 'alert');
        
        switch (type) {
            case 'valid':
                messageEl.className += ' bg-green-600/20 text-green-300 border border-green-600/30';
                break;
            case 'warning':
                messageEl.className += ' bg-yellow-600/20 text-yellow-300 border border-yellow-600/30';
                break;
            case 'invalid':
                messageEl.className += ' bg-red-600/20 text-red-300 border border-red-600/30';
                break;
        }
        
        messageEl.textContent = message;
        input.parentNode.appendChild(messageEl);
        
        // Auto-remove after delay
        setTimeout(() => {
            if (messageEl.parentNode) {
                messageEl.style.opacity = '0';
                messageEl.style.transform = 'translateY(-10px)';
                setTimeout(() => messageEl.remove(), 300);
            }
        }, 4000);
    }

    clearInputMessage(input) {
        const existingMessage = input.parentNode.querySelector('.input-validation-message');
        if (existingMessage) {
            existingMessage.remove();
        }
    }

    // ========================================
    // Stock Buttons Enhancement
    // ========================================
    initializeStockButtons() {
        const stockButtons = document.querySelectorAll('.stock-btn, .stock-quick-btn');
        stockButtons.forEach(button => this.enhanceStockButton(button));
    }

    enhanceStockButton(button) {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const symbol = button.getAttribute('data-symbol');
            this.handleStockButtonClick(symbol, button);
        });
        
        // Add ripple effect
        button.addEventListener('click', (e) => this.createRippleEffect(e, button));
    }

    handleStockButtonClick(symbol, button) {
        const symbolInput = document.getElementById('symbol') || document.querySelector('input[name="symbol"]');
        
        if (symbolInput && symbol) {
            // Animate selection
            this.animateStockSelection(button);
            
            // Update input
            symbolInput.value = symbol;
            symbolInput.focus();
            
            // Trigger validation
            symbolInput.dispatchEvent(new Event('input', { bubbles: true }));
            
            // Show feedback
            this.showNotification(`Selected ${symbol}`, 'info', 2000);
            
            // Highlight submit button
            setTimeout(() => this.highlightSubmitButton(), 500);
        }
    }

    animateStockSelection(button) {
        button.classList.add('animate-pulse', 'ring-2', 'ring-blue-400');
        
        setTimeout(() => {
            button.classList.remove('animate-pulse', 'ring-2', 'ring-blue-400');
        }, 1000);
    }

    createRippleEffect(event, element) {
        const ripple = document.createElement('div');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple 0.6s linear;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }

    highlightSubmitButton() {
        const submitBtn = document.getElementById('submitBtn') || document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.classList.add('animate-pulse', 'ring-4', 'ring-blue-400');
            setTimeout(() => {
                submitBtn.classList.remove('animate-pulse', 'ring-4', 'ring-blue-400');
            }, 2000);
        }
    }

    // ========================================
    // Chart Management System
    // ========================================
    initializeCharts() {
        // Wait for Chart.js to be available
        if (typeof Chart !== 'undefined') {
            this.setupChartDefaults();
            this.enhanceExistingCharts();
        } else {
            // Retry after a short delay
            setTimeout(() => this.initializeCharts(), 500);
        }
    }

    setupChartDefaults() {
        Chart.defaults.color = '#e5e7eb';
        Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
        Chart.defaults.responsive = true;
        Chart.defaults.maintainAspectRatio = false;
        Chart.defaults.plugins.legend.labels.usePointStyle = true;
    }

    enhanceExistingCharts() {
        const chartCanvases = document.querySelectorAll('canvas[id$="Chart"]');
        chartCanvases.forEach(canvas => this.enhanceChart(canvas));
    }

    enhanceChart(canvas) {
        if (!canvas) return;
        
        // Add hover effects
        canvas.addEventListener('mouseenter', () => {
            canvas.style.transform = 'scale(1.02)';
            canvas.style.transition = 'transform 0.3s ease';
        });
        
        canvas.addEventListener('mouseleave', () => {
            canvas.style.transform = 'scale(1)';
        });
        
        // Add loading state
        this.addChartLoadingState(canvas);
    }

    addChartLoadingState(canvas) {
        const container = canvas.parentElement;
        if (!container) return;
        
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'chart-loading-state';
        loadingDiv.innerHTML = `
            <div class="loading-spinner"></div>
            <p class="text-gray-400 mt-4">Loading chart data...</p>
        `;
        
        container.appendChild(loadingDiv);
        
        // Remove loading state when chart is ready
        setTimeout(() => {
            if (loadingDiv.parentNode) {
                loadingDiv.remove();
            }
        }, 2000);
    }

    // ========================================
    // Notification System
    // ========================================
    initializeNotifications() {
        // Create notification container if it doesn't exist
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.className = 'fixed top-20 right-4 z-50 space-y-2';
            container.setAttribute('aria-live', 'polite');
            document.body.appendChild(container);
        }
        
        // Handle flash messages
        this.handleFlashMessages();
    }

    handleFlashMessages() {
        const flashMessages = document.querySelectorAll('[data-flash-message]');
        flashMessages.forEach(message => {
            const dismissButton = message.querySelector('[data-dismiss]');
            if (dismissButton) {
                dismissButton.addEventListener('click', () => this.dismissFlashMessage(message));
            }
            
            // Auto-dismiss after timeout
            setTimeout(() => {
                if (message.parentElement) {
                    this.dismissFlashMessage(message);
                }
            }, this.config.notificationTimeout);
        });
    }

    dismissFlashMessage(message) {
        message.style.transform = 'translateX(100%)';
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 300);
    }

    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('notification-container');
        if (!container) return;

        const id = `notification-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const notification = document.createElement('div');
        notification.id = id;
        notification.className = `notification max-w-sm bg-white/10 backdrop-blur-lg rounded-lg shadow-lg border border-white/20 p-4 transform transition-all duration-300 ${this.getNotificationClasses(type)}`;
        
        notification.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <i class="fas ${this.getNotificationIcon(type)} mr-3"></i>
                    <span class="text-white font-medium">${message}</span>
                </div>
                <button class="ml-4 text-gray-300 hover:text-white transition-colors" onclick="window.stockApp.dismissNotification('${id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Store in state
        this.state.notifications.set(id, notification);
        
        container.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.classList.add('show');
        });
        
        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => this.dismissNotification(id), duration);
        }
        
        return id;
    }

    getNotificationClasses(type) {
        switch (type) {
            case 'success': return 'border-green-500/50';
            case 'error': return 'border-red-500/50';
            case 'warning': return 'border-yellow-500/50';
            default: return 'border-blue-500/50';
        }
    }

    getNotificationIcon(type) {
        switch (type) {
            case 'success': return 'fa-check-circle text-green-400';
            case 'error': return 'fa-exclamation-triangle text-red-400';
            case 'warning': return 'fa-exclamation-circle text-yellow-400';
            default: return 'fa-info-circle text-blue-400';
        }
    }

    dismissNotification(id) {
        const notification = this.state.notifications.get(id);
        if (notification) {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.remove();
                this.state.notifications.delete(id);
            }, 300);
        }
    }

    // ========================================
    // Loading Overlay System
    // ========================================
    showLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.remove('hidden');
            overlay.classList.add('flex');
        } else {
            this.createLoadingOverlay();
        }
    }

    hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.add('hidden');
            overlay.classList.remove('flex');
        }
    }

    createLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center';
        overlay.innerHTML = `
            <div class="bg-white/10 rounded-2xl p-8 max-w-sm mx-4 text-center glass-effect">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                <h3 class="text-white font-semibold text-lg mb-2">Processing Request</h3>
                <p class="text-gray-300 text-sm">Training AI model and generating predictions...</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    // ========================================
    // Keyboard Shortcuts
    // ========================================
    handleKeyboardShortcuts(e) {
        // Global shortcuts
        if (e.altKey) {
            switch (e.key) {
                case 'h':
                    e.preventDefault();
                    this.navigateToHome();
                    break;
                case 'd':
                    e.preventDefault();
                    this.navigateToDashboard();
                    break;
                case 'l':
                    e.preventDefault();
                    this.handleLogoutShortcut();
                    break;
            }
        }
        
        // Context-specific shortcuts
        if (e.key === 'Escape') {
            this.handleEscapeKey();
        }
        
        if (e.key === 'Enter' && e.target.id === 'symbol') {
            this.handleSymbolEnter(e);
        }
        
        // Quick stock selection shortcuts
        if (e.altKey && /^[1-8]$/.test(e.key)) {
            this.handleQuickStockSelection(e.key);
        }
    }

    navigateToHome() {
        window.location.href = '/';
    }

    navigateToDashboard() {
        if (document.body.dataset.authenticated === 'true') {
            window.location.href = '/dashboard';
        }
    }

    handleLogoutShortcut() {
        if (document.body.dataset.authenticated === 'true') {
            if (confirm('Are you sure you want to log out?')) {
                window.location.href = '/logout';
            }
        }
    }

    handleEscapeKey() {
        // Close modals
        this.closeAllModals();
        
        // Clear active inputs
        const activeInput = document.activeElement;
        if (activeInput && activeInput.tagName === 'INPUT') {
            activeInput.blur();
        }
        
        // Close mobile menu
        const mobileMenu = document.getElementById('mobile-menu');
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        if (mobileMenu && mobileMenu.classList.contains('show')) {
            this.closeMobileMenu(mobileMenu, mobileMenuButton, mobileMenuButton?.querySelector('i'));
        }
    }

    handleSymbolEnter(e) {
        const symbol = e.target.value.trim();
        if (symbol.length >= 2) {
            const form = e.target.closest('form');
            if (form) {
                form.submit();
            }
        }
    }

    handleQuickStockSelection(key) {
        const stockMap = {
            '1': 'AAPL', '2': 'GOOGL', '3': 'TSLA', '4': 'MSFT',
            '5': 'AMZN', '6': 'META', '7': 'NFLX', '8': 'NVDA'
        };
        
        const symbol = stockMap[key];
        const symbolInput = document.getElementById('symbol');
        
        if (symbol && symbolInput) {
            symbolInput.value = symbol;
            symbolInput.focus();
            symbolInput.dispatchEvent(new Event('input', { bubbles: true }));
            this.showNotification(`Selected ${symbol}`, 'info', 2000);
        }
    }

    // ========================================
    // Modal System
    // ========================================
    initializeModals() {
        const modals = document.querySelectorAll('[data-modal]');
        modals.forEach(modal => this.enhanceModal(modal));
    }

    enhanceModal(modal) {
        const closeButtons = modal.querySelectorAll('[data-close-modal]');
        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.closeModal(modal));
        });
        
        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal(modal);
            }
        });
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            this.state.activeModals.add(modalId);
            document.body.style.overflow = 'hidden';
        }
    }

    closeModal(modal) {
        const modalId = modal.id;
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        this.state.activeModals.delete(modalId);
        
        if (this.state.activeModals.size === 0) {
            document.body.style.overflow = '';
        }
    }

    closeAllModals() {
        this.state.activeModals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (modal) {
                this.closeModal(modal);
            }
        });
    }

    // ========================================
    // Table Interactions
    // ========================================
    initializeTableInteractions() {
        const tableRows = document.querySelectorAll('tbody tr[data-href], tbody tr[onclick]');
        tableRows.forEach(row => this.enhanceTableRow(row));
    }

    enhanceTableRow(row) {
        row.style.cursor = 'pointer';
        
        // Add hover effects
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'translateX(4px)';
            row.style.background = 'rgba(255, 255, 255, 0.08)';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'translateX(0)';
            row.style.background = '';
        });
        
        // Add keyboard navigation
        row.setAttribute('tabindex', '0');
        row.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                row.click();
            }
        });
    }

    // ========================================
    // Page-Specific Initializers
    // ========================================
    initializeDashboard() {
        console.log('📊 Initializing Dashboard...');
        
        // Enhanced welcome message
        this.showDashboardWelcome();
        
        // Initialize prediction form if present
        const predictionForm = document.getElementById('predictionForm');
        if (predictionForm) {
            this.enhancePredictionForm(predictionForm);
        }
        
        // Initialize recent predictions interactions
        this.initializeRecentPredictions();
    }

    initializePredictionPage() {
        console.log('🔮 Initializing Prediction Page...');
        
        // Initialize charts
        this.initializeCharts();
        
        // Add print functionality
        this.initializePrintFunctionality();
        
        // Initialize chart interactions
        this.initializeChartInteractions();
    }

    initializeHistoryPage() {
        console.log('📈 Initializing History Page...');
        
        // Initialize table interactions
        this.initializeTableInteractions();
        
        // Initialize pagination
        this.initializePagination();
        
        // Initialize search/filter functionality
        this.initializeHistorySearch();
    }

    initializeProfilePage() {
        console.log('👤 Initializing Profile Page...');
        
        // Initialize password change modal
        this.initializePasswordModal();
        
        // Initialize data export functionality
        this.initializeDataExport();
        
        // Initialize account management
        this.initializeAccountManagement();
    }

    initializeAuthPages() {
        console.log('🔐 Initializing Auth Page...');
        
        // Initialize password visibility toggle
        this.initializePasswordToggle();
        
        // Initialize password strength checker
        this.initializePasswordStrength();
        
        // Auto-focus first input
        const firstInput = document.querySelector('input[type="text"], input[type="email"]');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }

    initializeGeneralPage() {
        console.log('🏠 Initializing General Page...');
        
        // Initialize hero animations
        this.initializeHeroAnimations();
        
        // Initialize feature showcases
        this.initializeFeatureShowcases();
    }

    // ========================================
    // Enhanced Form Features
    // ========================================
    enhancePredictionForm(form) {
        // Add real-time validation
        const symbolInput = form.querySelector('#symbol, input[name="symbol"]');
        if (symbolInput) {
            symbolInput.addEventListener('input', () => {
                const isValid = this.validatePredictionForm(form);
                this.toggleSubmitButton(form, isValid);
            });
        }
        
        // Add form progress indication
        this.addFormProgressIndicator(form);
    }

    validatePredictionForm(form) {
        const symbolInput = form.querySelector('#symbol, input[name="symbol"]');
        const symbol = symbolInput?.value.trim();
        
        return symbol && symbol.length >= 2 && symbol.length <= 5 && /^[A-Z]+$/.test(symbol);
    }

    toggleSubmitButton(form, isValid) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = !isValid;
            submitButton.classList.toggle('opacity-50', !isValid);
        }
    }

    addFormProgressIndicator(form) {
        // Create progress bar
        const progressBar = document.createElement('div');
        progressBar.className = 'form-progress-bar fixed top-0 left-0 h-1 bg-blue-500 transition-all duration-300 z-50';
        progressBar.style.width = '0%';
        document.body.appendChild(progressBar);
        
        form.addEventListener('submit', () => {
            this.animateProgressBar(progressBar);
        });
    }

    animateProgressBar(progressBar) {
        const stages = [10, 25, 40, 60, 80, 95];
        let currentStage = 0;
        
        const interval = setInterval(() => {
            if (currentStage < stages.length) {
                progressBar.style.width = `${stages[currentStage]}%`;
                currentStage++;
            } else {
                clearInterval(interval);
                setTimeout(() => {
                    progressBar.style.width = '100%';
                    setTimeout(() => {
                        progressBar.remove();
                    }, 500);
                }, 1000);
            }
        }, 800);
    }

    // ========================================
    // Auto-Save Functionality
    // ========================================
    initializeAutoSave() {
        const autoSaveForms = document.querySelectorAll('form[data-autosave]');
        autoSaveForms.forEach(form => this.enableAutoSave(form));
    }

    enableAutoSave(form) {
        const formId = form.id || `form-${Date.now()}`;
        const saveKey = `autosave-${formId}`;
        const excludeFields = ['csrf_token', 'password', 'password2'];
        
        // Load saved data
        this.loadAutoSavedData(form, saveKey, excludeFields);
        
        // Save data on input
        form.addEventListener('input', this.debounce(() => {
            this.saveFormData(form, saveKey, excludeFields);
        }, 1000));
        
        // Clear saved data on successful submit
        form.addEventListener('submit', () => {
            setTimeout(() => this.clearAutoSavedData(saveKey), 1000);
        });
    }

    loadAutoSavedData(form, saveKey, excludeFields) {
        try {
            const savedData = localStorage.getItem(saveKey);
            if (savedData) {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(name => {
                    if (!excludeFields.includes(name)) {
                        const field = form.querySelector(`[name="${name}"]`);
                        if (field && field.type !== 'password') {
                            field.value = data[name];
                        }
                    }
                });
            }
        } catch (e) {
            console.warn('Could not load auto-saved data:', e);
        }
    }

    saveFormData(form, saveKey, excludeFields) {
        try {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                if (!excludeFields.includes(key)) {
                    data[key] = value;
                }
            }
            localStorage.setItem(saveKey, JSON.stringify(data));
        } catch (e) {
            console.warn('Could not save form data:', e);
        }
    }

    clearAutoSavedData(saveKey) {
        try {
            localStorage.removeItem(saveKey);
        } catch (e) {
            console.warn('Could not clear auto-saved data:', e);
        }
    }

    // ========================================
    // Input Enhancement Functions
    // ========================================
    handleInputFocus(e) {
        const input = e.target;
        input.classList.add('ring-2', 'ring-blue-500');
        input.style.boxShadow = '0 0 20px rgba(59, 130, 246, 0.3)';
        input.style.transform = 'translateY(-1px)';
    }

    handleInputBlur(e) {
        const input = e.target;
        input.classList.remove('ring-2', 'ring-blue-500');
        input.style.boxShadow = '';
        input.style.transform = '';
    }

    handleInputChange(e) {
        const input = e.target;
        
        // Add changed indicator
        if (input.value !== (input.dataset.originalValue || '')) {
            input.classList.add('border-yellow-500');
        } else {
            input.classList.remove('border-yellow-500');
        }
    }

    initializeInputValidation() {
        const inputs = document.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.dataset.originalValue = input.value;
            
            input.addEventListener('invalid', (e) => {
                e.preventDefault();
                this.showInputError(input, input.validationMessage);
            });
            
            input.addEventListener('input', () => {
                if (input.checkValidity()) {
                    this.clearInputError(input);
                }
            });
        });
    }

    showInputError(input, message) {
        this.clearInputError(input);
        input.classList.add('ring-2', 'ring-red-500');
        
        const errorEl = document.createElement('div');
        errorEl.className = 'input-error text-red-400 text-sm mt-1';
        errorEl.innerHTML = `<i class="fas fa-exclamation-circle mr-1"></i>${message}`;
        input.parentNode.appendChild(errorEl);
    }

    clearInputError(input) {
        input.classList.remove('ring-2', 'ring-red-500');
        const errorEl = input.parentNode.querySelector('.input-error');
        if (errorEl) {
            errorEl.remove();
        }
    }

    // ========================================
    // Accessibility Enhancements
    // ========================================
    initializeAccessibility() {
        // Skip to main content link
        this.addSkipToMainContent();
        
        // Keyboard navigation for dropdowns
        this.enhanceDropdownNavigation();
        
        // Announce page changes
        this.announcePageChanges();
        
        // Focus management
        this.initializeFocusManagement();
    }

    addSkipToMainContent() {
        const existingSkipLink = document.querySelector('.sr-only[href="#main-content"]');
        if (!existingSkipLink) {
            const skipLink = document.createElement('a');
            skipLink.href = '#main-content';
            skipLink.className = 'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-blue-600 text-white px-4 py-2 rounded-lg z-50';
            skipLink.textContent = 'Skip to main content';
            document.body.insertBefore(skipLink, document.body.firstChild);
        }
    }

    enhanceDropdownNavigation() {
        const dropdownButtons = document.querySelectorAll('[aria-haspopup="true"]');
        dropdownButtons.forEach(button => {
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    button.click();
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    this.focusFirstDropdownItem(button);
                }
            });
        });
    }

    focusFirstDropdownItem(button) {
        const dropdown = button.nextElementSibling || document.querySelector(`[aria-labelledby="${button.id}"]`);
        if (dropdown) {
            const firstItem = dropdown.querySelector('a, button');
            if (firstItem) {
                firstItem.focus();
            }
        }
    }

    announcePageChanges() {
        const pageTitle = document.title;
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = `Page loaded: ${pageTitle}`;
        document.body.appendChild(announcement);
        
        setTimeout(() => announcement.remove(), 3000);
    }

    initializeFocusManagement() {
        // Focus management for modals
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                this.manageFocusInModals(e);
            }
        });
    }

    manageFocusInModals(e) {
        const activeModal = Array.from(this.state.activeModals).map(id => document.getElementById(id)).find(modal => modal && !modal.classList.contains('hidden'));
        
        if (activeModal) {
            const focusableElements = activeModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            const firstFocusableElement = focusableElements[0];
            const lastFocusableElement = focusableElements[focusableElements.length - 1];
            
            if (e.shiftKey && document.activeElement === firstFocusableElement) {
                e.preventDefault();
                lastFocusableElement.focus();
            } else if (!e.shiftKey && document.activeElement === lastFocusableElement) {
                e.preventDefault();
                firstFocusableElement.focus();
            }
        }
    }

    // ========================================
    // Performance Optimizations
    // ========================================
    initializePerformanceOptimizations() {
        // Image lazy loading
        this.initializeLazyLoading();
        
        // Resource hints
        this.addResourceHints();
        
        // Performance monitoring
        this.initializePerformanceMonitoring();
    }

    initializeLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for older browsers
            images.forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    }

    addResourceHints() {
        // Preconnect to external domains
        const preconnectDomains = [
            'https://cdn.jsdelivr.net',
            'https://cdnjs.cloudflare.com',
            'https://fonts.googleapis.com',
            'https://fonts.gstatic.com'
        ];
        
        preconnectDomains.forEach(domain => {
            const link = document.createElement('link');
            link.rel = 'preconnect';
            link.href = domain;
            document.head.appendChild(link);
        });
    }

    initializePerformanceMonitoring() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
                console.log(`📊 Page loaded in ${loadTime}ms`);
                
                // Show warning for slow loads
                if (loadTime > 5000) {
                    setTimeout(() => {
                        this.showNotification('Page loaded slower than expected. Please check your connection.', 'warning');
                    }, 1000);
                }
            });
        }
    }

    // ========================================
    // Welcome Message System
    // ========================================
    showWelcomeMessage() {
        const userElement = document.querySelector('[data-user-info]');
        if (userElement) {
            const memberSince = userElement.dataset.memberSince;
            const now = new Date();
            const memberDate = new Date(memberSince);
            const daysSinceMember = Math.floor((now - memberDate) / (1000 * 60 * 60 * 24));
            
            if (daysSinceMember === 0) {
                setTimeout(() => {
                    this.showNotification('Welcome to AI Stock Predictor! 🎉', 'success');
                }, 2000);
            }
        }
    }

    showDashboardWelcome() {
        const hour = new Date().getHours();
        let greeting = 'Good evening';
        
        if (hour < 12) greeting = 'Good morning';
        else if (hour < 18) greeting = 'Good afternoon';
        
        setTimeout(() => {
            this.showNotification(`${greeting}! Ready to predict some stocks?`, 'info', 3000);
        }, 1500);
    }

    // ========================================
    // Utility Functions
    // ========================================
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

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // ========================================
    // Event Handlers
    // ========================================
    handleResize() {
        // Update chart dimensions
        this.updateChartDimensions();
        
        // Update mobile menu state
        this.updateMobileMenuState();
        
        // Recalculate animations
        this.recalculateAnimations();
    }

    handleScroll() {
        // Update header opacity
        this.updateHeaderOpacity();
        
        // Trigger scroll animations
        this.triggerScrollAnimations();
    }

    handleBeforeUnload() {
        // Save form data
        this.saveAllFormData();
        
        // Clean up resources
        this.cleanup();
    }

    handleError(event) {
        console.error('JavaScript Error:', event.error);
        this.showNotification('An unexpected error occurred. Please refresh the page.', 'error');
    }

    handlePromiseRejection(event) {
        console.error('Promise Rejection:', event.reason);
        this.showNotification('A network error occurred. Please check your connection.', 'error');
    }

    handleGlobalClick(event) {
        // Close dropdowns when clicking outside
        this.closeOpenDropdowns(event);
        
        // Handle dynamic elements
        this.handleDynamicClicks(event);
    }

    // ========================================
    // Additional Feature Implementations
    // ========================================
    initializePasswordToggle() {
        const toggleButtons = document.querySelectorAll('[data-password-toggle]');
        toggleButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetId = button.dataset.passwordToggle;
                const passwordField = document.getElementById(targetId);
                const icon = button.querySelector('i');
                
                if (passwordField.type === 'password') {
                    passwordField.type = 'text';
                    icon.classList.replace('fa-eye', 'fa-eye-slash');
                } else {
                    passwordField.type = 'password';
                    icon.classList.replace('fa-eye-slash', 'fa-eye');
                }
            });
        });
    }

    initializePasswordStrength() {
        const passwordFields = document.querySelectorAll('input[type="password"][data-strength]');
        passwordFields.forEach(field => {
            field.addEventListener('input', (e) => {
                this.updatePasswordStrength(e.target);
            });
        });
    }

    updatePasswordStrength(passwordField) {
        const password = passwordField.value;
        const strength = this.calculatePasswordStrength(password);
        const indicator = passwordField.parentNode.querySelector('.password-strength-indicator');
        
        if (indicator) {
            this.updateStrengthIndicator(indicator, strength);
        }
    }

    calculatePasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 8) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;
        
        return Math.min(strength, 4);
    }

    updateStrengthIndicator(indicator, strength) {
        const bars = indicator.querySelectorAll('.strength-bar');
        const texts = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
        const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'];
        
        bars.forEach((bar, index) => {
            bar.className = `strength-bar h-1 w-1/4 rounded ${index < strength ? colors[strength - 1] : 'bg-gray-600'}`;
        });
        
        const textElement = indicator.querySelector('.strength-text');
        if (textElement && strength > 0) {
            textElement.textContent = texts[strength - 1];
            textElement.className = `strength-text text-xs mt-1 ${strength >= 3 ? 'text-green-400' : strength >= 2 ? 'text-yellow-400' : 'text-red-400'}`;
        }
    }

    initializePrintFunctionality() {
        const printButtons = document.querySelectorAll('[data-print]');
        printButtons.forEach(button => {
            button.addEventListener('click', () => {
                this.handlePrint();
            });
        });
    }

    handlePrint() {
        // Prepare page for printing
        document.body.classList.add('print-mode');
        
        // Hide non-printable elements
        const noPrintElements = document.querySelectorAll('.no-print');
        noPrintElements.forEach(el => el.style.display = 'none');
        
        // Print
        window.print();
        
        // Restore after printing
        setTimeout(() => {
            document.body.classList.remove('print-mode');
            noPrintElements.forEach(el => el.style.display = '');
        }, 1000);
    }

    initializeChartInteractions() {
        const charts = document.querySelectorAll('canvas[id$="Chart"]');
        charts.forEach(chart => {
            chart.addEventListener('click', (e) => this.handleChartClick(e, chart));
        });
    }

    handleChartClick(event, chart) {
        // Add click interaction feedback
        const rect = chart.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        
        this.createChartClickEffect(chart, x, y);
    }

    createChartClickEffect(chart, x, y) {
        const effect = document.createElement('div');
        effect.style.cssText = `
            position: absolute;
            left: ${x}px;
            top: ${y}px;
            width: 20px;
            height: 20px;
            background: rgba(59, 130, 246, 0.5);
            border-radius: 50%;
            transform: translate(-50%, -50%) scale(0);
            animation: chartClickEffect 0.6s ease-out forwards;
            pointer-events: none;
            z-index: 10;
        `;
        
        chart.parentElement.style.position = 'relative';
        chart.parentElement.appendChild(effect);
        
        setTimeout(() => effect.remove(), 600);
    }

    initializePagination() {
        const paginationLinks = document.querySelectorAll('.pagination a[href]');
        paginationLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                this.handlePaginationClick(e, link);
            });
        });
    }

    handlePaginationClick(event, link) {
        event.preventDefault();
        
        // Add loading state
        link.classList.add('opacity-50', 'pointer-events-none');
        
        // Navigate to page
        window.location.href = link.href;
    }

    initializeHistorySearch() {
        const searchInput = document.querySelector('[data-search="history"]');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.performHistorySearch(e.target.value);
            }, 300));
        }
    }

    performHistorySearch(query) {
        const rows = document.querySelectorAll('tbody tr[data-searchable]');
        const lowerQuery = query.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const matches = text.includes(lowerQuery);
            row.style.display = matches ? '' : 'none';
        });
        
        // Update results count
        const visibleRows = Array.from(rows).filter(row => row.style.display !== 'none').length;
        this.updateSearchResults(visibleRows, rows.length);
    }

    updateSearchResults(visible, total) {
        const resultsElement = document.querySelector('[data-search-results]');
        if (resultsElement) {
            resultsElement.textContent = `Showing ${visible} of ${total} predictions`;
        }
    }

    // ========================================
    // Profile Page Features
    // ========================================
    initializePasswordModal() {
        const passwordModal = document.getElementById('passwordModal');
        const openButton = document.querySelector('[data-open="passwordModal"]');
        const form = document.getElementById('passwordForm');
        
        if (openButton) {
            openButton.addEventListener('click', () => this.openModal('passwordModal'));
        }
        
        if (form) {
            form.addEventListener('submit', (e) => this.handlePasswordChange(e));
        }
    }

    handlePasswordChange(event) {
        event.preventDefault();
        
        const form = event.target;
        const currentPassword = form.querySelector('#currentPassword').value;
        const newPassword = form.querySelector('#newPassword').value;
        const confirmPassword = form.querySelector('#confirmPassword').value;
        
        // Validation
        if (newPassword !== confirmPassword) {
            this.showNotification('New passwords do not match', 'error');
            return;
        }
        
        if (newPassword.length < 6) {
            this.showNotification('Password must be at least 6 characters long', 'error');
            return;
        }
        
        // Mock password change (replace with actual API call)
        this.showNotification('Password change functionality would be implemented here', 'info');
        this.closeModal(document.getElementById('passwordModal'));
        form.reset();
    }

    initializeDataExport() {
        const exportButton = document.querySelector('[data-export="user-data"]');
        if (exportButton) {
            exportButton.addEventListener('click', () => this.handleDataExport());
        }
    }

    handleDataExport() {
        this.showNotification('Preparing your data export...', 'info');
        
        // Create mock export data
        const exportData = {
            exportDate: new Date().toISOString(),
            userData: {
                profile: 'User profile data would be here',
                predictions: 'Prediction history would be here',
                settings: 'User settings would be here'
            },
            note: 'This is a sample export. In production, this would contain real user data.'
        };
        
        // Create and download file
        const dataStr = JSON.stringify(exportData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = `stock-predictor-data-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        this.showNotification('Data export downloaded successfully!', 'success');
    }

    initializeAccountManagement() {
        const deleteButton = document.querySelector('[data-action="delete-account"]');
        if (deleteButton) {
            deleteButton.addEventListener('click', () => this.handleAccountDeletion());
        }
    }

    handleAccountDeletion() {
        const confirmations = [
            'Are you sure you want to delete your account?',
            'This will permanently delete all your data. Continue?',
            'Type "DELETE" to confirm account deletion:'
        ];
        
        if (confirm(confirmations[0])) {
            if (confirm(confirmations[1])) {
                const confirmation = prompt(confirmations[2]);
                if (confirmation === 'DELETE') {
                    this.showNotification('Account deletion would be processed here', 'warning');
                } else {
                    this.showNotification('Account deletion cancelled', 'info');
                }
            }
        }
    }

    // ========================================
    // Cleanup and Resource Management
    // ========================================
    updateChartDimensions() {
        if (typeof Chart !== 'undefined') {
            Chart.instances.forEach(chart => {
                if (chart && chart.resize) {
                    chart.resize();
                }
            });
        }
    }

    updateMobileMenuState() {
        const mobileMenu = document.getElementById('mobile-menu');
        if (mobileMenu && window.innerWidth > 768) {
            mobileMenu.classList.remove('show');
        }
    }

    recalculateAnimations() {
        // Recalculate animation timing for responsive design
        const animatedElements = document.querySelectorAll('[style*="animation-delay"]');
        animatedElements.forEach(el => {
            const delay = parseInt(el.style.animationDelay) || 0;
            el.style.animationDelay = `${Math.min(delay, 1000)}ms`;
        });
    }

    updateHeaderOpacity() {
        const header = document.querySelector('nav');
        if (header) {
            const scrollTop = window.pageYOffset;
            const opacity = Math.min(scrollTop / 100, 1);
            header.style.backgroundColor = `rgba(15, 23, 42, ${0.8 + (opacity * 0.2)})`;
        }
    }

    triggerScrollAnimations() {
        // Trigger animations for elements coming into view
        const elements = document.querySelectorAll('.animate-on-scroll:not(.animated)');
        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                el.classList.add('animated', 'animate-fade-in');
            }
        });
    }

    saveAllFormData() {
        const forms = document.querySelectorAll('form[data-autosave]');
        forms.forEach(form => {
            const formId = form.id || `form-${Date.now()}`;
            const saveKey = `autosave-${formId}`;
            this.saveFormData(form, saveKey, ['csrf_token', 'password', 'password2']);
        });
    }

    closeOpenDropdowns(event) {
        const dropdowns = document.querySelectorAll('[aria-expanded="true"]');
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(event.target)) {
                dropdown.setAttribute('aria-expanded', 'false');
                const menu = dropdown.nextElementSibling || document.querySelector(`[aria-labelledby="${dropdown.id}"]`);
                if (menu) {
                    menu.classList.add('hidden');
                }
            }
        });
    }

    handleDynamicClicks(event) {
        // Handle clicks on dynamically added elements
        const target = event.target.closest('[data-dynamic-action]');
        if (target) {
            const action = target.dataset.dynamicAction;
            this.handleDynamicAction(action, target, event);
        }
    }

    handleDynamicAction(action, element, event) {
        switch (action) {
            case 'dismiss-notification':
                this.dismissNotification(element.dataset.notificationId);
                break;
            case 'toggle-modal':
                this.toggleModal(element.dataset.modal);
                break;
            case 'copy-text':
                this.copyTextToClipboard(element.dataset.text);
                break;
        }
    }

    copyTextToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success', 2000);
            });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showNotification('Copied to clipboard!', 'success', 2000);
        }
    }

    cleanup() {
        // Cleanup intervals and observers
        if (this.intersectionObserver) {
            this.intersectionObserver.disconnect();
        }
        
        // Clear any remaining timeouts
        this.state.notifications.forEach((notification, id) => {
            if (notification.timeout) {
                clearTimeout(notification.timeout);
            }
        });
        
        // Remove event listeners
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('scroll', this.handleScroll);
    }

    // ========================================
    // Public API Methods
    // ========================================
    getVersion() {
        return this.version;
    }

    getState() {
        return { ...this.state };
    }

    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
    }

    // For external access
    dismissNotification(id) {
        return this.dismissNotification(id);
    }

    showNotification(message, type, duration) {
        return this.showNotification(message, type, duration);
    }
}

// ========================================
// CSS Animation Definitions
// ========================================
const animationCSS = `
@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

@keyframes chartClickEffect {
    0% {
        transform: translate(-50%, -50%) scale(0);
        opacity: 1;
    }
    100% {
        transform: translate(-50%, -50%) scale(3);
        opacity: 0;
    }
}

.form-progress-bar {
    transition: width 0.8s ease;
}

.notification {
    transform: translateX(100%);
}

.notification.show {
    transform: translateX(0);
}
`;

// Inject animation CSS
const styleSheet = document.createElement('style');
styleSheet.textContent = animationCSS;
document.head.appendChild(styleSheet);

// ========================================
// Service Worker Registration (Optional)
// ========================================
if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered:', registration);
            })
            .catch(error => {
                console.log('SW registration failed:', error);
            });
    });
}

// ========================================
// Initialize Application
// ========================================
let stockApp;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        stockApp = new StockPredictorApp();
        window.stockApp = stockApp; // Make globally accessible
    });
} else {
    stockApp = new StockPredictorApp();
    window.stockApp = stockApp;
}

// ========================================
// Global Utility Functions (for template use)
// ========================================
window.showLoadingOverlay = () => stockApp?.showLoadingOverlay();
window.hideLoadingOverlay = () => stockApp?.hideLoadingOverlay();
window.showNotification = (message, type, duration) => stockApp?.showNotification(message, type, duration);
window.dismissNotification = (id) => stockApp?.dismissNotification(id);

// Legacy compatibility functions
function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    const icon = document.querySelector(`[data-password-toggle="${fieldId}"] i`);
    
    if (field && icon) {
        if (field.type === 'password') {
            field.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            field.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    }
}

function changePassword() {
    stockApp?.openModal('passwordModal');
}

function closePasswordModal() {
    stockApp?.closeModal(document.getElementById('passwordModal'));
}

function exportData() {
    stockApp?.handleDataExport();
}

function deleteAccount() {
    stockApp?.handleAccountDeletion();
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StockPredictorApp;
}

console.log('🚀 AI Stock Predictor JavaScript loaded successfully');