/**
 * Theme Toggle & Interactive Features Script
 * -------------------------------------------
 * Handles dark mode, modals, charts, and quick-fill functionality
 */

(function () {
    'use strict';

    // ============ DOM Elements ============
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Help Modal Elements
    const helpBtn = document.getElementById('helpBtn');
    const helpModal = document.getElementById('helpModal');
    const closeModal = document.getElementById('closeModal');
    const closeModalBtn = document.getElementById('closeModalBtn');

    // Chart Modal Elements
    const showChartBtn = document.getElementById('showChartBtn');
    const chartModal = document.getElementById('chartModal');
    const closeChartModal = document.getElementById('closeChartModal');
    const chartTitle = document.getElementById('chartTitle');
    const chartLoading = document.getElementById('chartLoading');
    const chartImage = document.getElementById('chartImage');
    const chartButtons = document.querySelectorAll('.btn-chart');

    // Quick Fill Elements
    const quickFillCards = document.querySelectorAll('.quick-fill-card');

    // Form Inputs
    const sepalLength = document.getElementById('sepal_length');
    const sepalWidth = document.getElementById('sepal_width');
    const petalLength = document.getElementById('petal_length');
    const petalWidth = document.getElementById('petal_width');

    // ============ Theme Constants ============
    const THEME_KEY = 'iris-predictor-theme';
    const DARK_MODE_CLASS = 'dark-mode';

    // ============ Theme Functions ============
    function initializeTheme() {
        const savedTheme = localStorage.getItem(THEME_KEY);

        if (savedTheme === 'dark') {
            body.classList.add(DARK_MODE_CLASS);
        } else if (savedTheme === 'light') {
            body.classList.remove(DARK_MODE_CLASS);
        } else {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            if (prefersDark) {
                body.classList.add(DARK_MODE_CLASS);
            }
        }
    }

    function toggleTheme() {
        body.classList.toggle(DARK_MODE_CLASS);
        const isDarkMode = body.classList.contains(DARK_MODE_CLASS);
        localStorage.setItem(THEME_KEY, isDarkMode ? 'dark' : 'light');
        animateToggle(themeToggle);
    }

    function animateToggle(element) {
        element.style.transform = 'scale(0.9)';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 150);
    }

    // ============ Modal Functions ============
    function openModal(modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModalFn(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Close modal when clicking outside
    function handleOutsideClick(e, modal) {
        if (e.target === modal) {
            closeModalFn(modal);
        }
    }

    // ============ Chart Functions ============
    let currentChart = null;

    async function loadChart(chartType) {
        // Show loading
        chartLoading.style.display = 'flex';
        chartImage.style.display = 'none';

        // Update title
        const titles = {
            '2d': '📈 2D Dataset Visualization',
            '3d': '🎲 3D Dataset Visualization',
            '3d/pca': '🧬 3D PCA Visualization'
        };
        chartTitle.textContent = titles[chartType] || '📊 Chart';

        // Update active button
        chartButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.chart === chartType);
        });

        try {
            const response = await fetch(`/chart/${chartType}`);
            const data = await response.json();

            if (data.success) {
                chartImage.src = `data:image/png;base64,${data.image}`;
                chartImage.style.display = 'block';
                chartLoading.style.display = 'none';
                currentChart = chartType;
            } else {
                throw new Error(data.error || 'Failed to load chart');
            }
        } catch (error) {
            console.error('Chart loading error:', error);
            chartLoading.innerHTML = `
                <div class="error-icon">❌</div>
                <p>Failed to load chart: ${error.message}</p>
                <button class="btn-primary" onclick="location.reload()">Retry</button>
            `;
        }
    }

    // ============ Quick Fill Functions ============
    function fillForm(sl, sw, pl, pw) {
        sepalLength.value = sl;
        sepalWidth.value = sw;
        petalLength.value = pl;
        petalWidth.value = pw;

        // Animate inputs
        [sepalLength, sepalWidth, petalLength, petalWidth].forEach(input => {
            input.style.transform = 'scale(1.05)';
            input.style.transition = 'transform 0.2s ease';
            setTimeout(() => {
                input.style.transform = 'scale(1)';
            }, 200);
        });

        // Scroll to form
        document.querySelector('.prediction-card').scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }

    // ============ Input Animations ============
    function setupInputAnimations() {
        const inputs = document.querySelectorAll('.input-group input');

        inputs.forEach(input => {
            input.addEventListener('focus', function () {
                this.parentElement.classList.add('focused');
            });

            input.addEventListener('blur', function () {
                this.parentElement.classList.remove('focused');
            });
        });
    }

    // ============ Button Effects ============
    function setupButtonEffects() {
        const buttons = document.querySelectorAll('.predict-btn, .chart-btn');

        buttons.forEach(btn => {
            btn.addEventListener('click', function (e) {
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');

                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = e.clientX - rect.left - size / 2 + 'px';
                ripple.style.top = e.clientY - rect.top - size / 2 + 'px';

                this.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            });
        });
    }

    // ============ Result Animation ============
    function setupResultAnimation() {
        const resultCard = document.querySelector('.result-card');

        if (resultCard) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                    }
                });
            }, { threshold: 0.1 });

            observer.observe(resultCard);
        }
    }

    // ============ Smooth Scroll to Result ============
    function setupSmoothScroll() {
        const resultSection = document.querySelector('.result-section');

        if (resultSection) {
            setTimeout(() => {
                resultSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }, 100);
        }
    }

    // ============ Info Card Effects ============
    function setupInfoCardEffects() {
        const infoCards = document.querySelectorAll('.info-card');

        infoCards.forEach(card => {
            card.addEventListener('mouseenter', function () {
                const emoji = this.querySelector('.info-emoji');
                if (emoji) {
                    emoji.style.transform = 'scale(1.2) rotate(10deg)';
                    emoji.style.transition = 'transform 0.3s ease';
                }
            });

            card.addEventListener('mouseleave', function () {
                const emoji = this.querySelector('.info-emoji');
                if (emoji) {
                    emoji.style.transform = 'scale(1) rotate(0deg)';
                }
            });
        });
    }

    // ============ Keyboard Navigation ============
    function setupKeyboardNav() {
        document.addEventListener('keydown', (e) => {
            // Close modals with Escape
            if (e.key === 'Escape') {
                if (helpModal.classList.contains('active')) {
                    closeModalFn(helpModal);
                }
                if (chartModal.classList.contains('active')) {
                    closeModalFn(chartModal);
                }
            }

            // Toggle theme with 'D' key
            if (e.key === 'd' || e.key === 'D') {
                if (!e.target.matches('input, textarea')) {
                    toggleTheme();
                }
            }
        });
    }

    // ============ Event Listeners ============

    // Theme toggle
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Help modal
    if (helpBtn) {
        helpBtn.addEventListener('click', () => openModal(helpModal));
    }
    if (closeModal) {
        closeModal.addEventListener('click', () => closeModalFn(helpModal));
    }
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => closeModalFn(helpModal));
    }
    if (helpModal) {
        helpModal.addEventListener('click', (e) => handleOutsideClick(e, helpModal));
    }

    // Chart modal
    if (showChartBtn) {
        showChartBtn.addEventListener('click', () => {
            openModal(chartModal);
            loadChart('2d'); // Load default chart
        });
    }
    if (closeChartModal) {
        closeChartModal.addEventListener('click', () => closeModalFn(chartModal));
    }
    if (chartModal) {
        chartModal.addEventListener('click', (e) => handleOutsideClick(e, chartModal));
    }

    // Chart type buttons
    chartButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            loadChart(btn.dataset.chart);
        });
    });

    // Quick fill cards
    quickFillCards.forEach(card => {
        card.addEventListener('click', () => {
            fillForm(
                card.dataset.sl,
                card.dataset.sw,
                card.dataset.pl,
                card.dataset.pw
            );
        });
    });

    // System theme change listener
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem(THEME_KEY)) {
            if (e.matches) {
                body.classList.add(DARK_MODE_CLASS);
            } else {
                body.classList.remove(DARK_MODE_CLASS);
            }
        }
    });

    // ============ Initialize ============
    document.addEventListener('DOMContentLoaded', function () {
        initializeTheme();
        setupInputAnimations();
        setupButtonEffects();
        setupResultAnimation();
        setupSmoothScroll();
        setupInfoCardEffects();
        setupKeyboardNav();
    });

    // ============ Additional Styles ============
    const style = document.createElement('style');
    style.textContent = `
        .predict-btn, .chart-btn {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .input-group.focused label {
            color: #667eea;
        }
        
        .info-card .info-emoji {
            transition: transform 0.3s ease;
        }
        
        .result-card.animate-in {
            animation: zoomIn 0.5s ease;
        }
        
        @keyframes zoomIn {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        .quick-fill-card:active {
            transform: scale(0.95);
        }
    `;
    document.head.appendChild(style);

})();
