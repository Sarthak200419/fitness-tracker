/* Main JavaScript */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Fitness Tracker loaded');
});

// Theme (dark/light) toggle
function applyTheme(theme) {
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
        const btn = document.getElementById('theme-toggle');
        if (btn) btn.textContent = '☀️';
    } else {
        document.documentElement.classList.remove('dark');
        const btn = document.getElementById('theme-toggle');
        if (btn) btn.textContent = '🌙';
    }
}

function toggleTheme() {
    const current = localStorage.getItem('ft_theme') || (document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    const next = current === 'dark' ? 'light' : 'dark';
    localStorage.setItem('ft_theme', next);
    applyTheme(next);
}

// Apply saved theme on load and wire the toggle
document.addEventListener('DOMContentLoaded', function() {
    const saved = localStorage.getItem('ft_theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(saved);
    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleTheme();
        });
        // keyboard accessible
        toggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }
});

// Utility: Format date
function formatDate(date) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

// Utility: Format time
function formatTime(date) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(date).toLocaleTimeString('en-US', options);
}

// Utility: Fetch with error handling
async function fetchWithErrorHandling(url, options = {}) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Utility: Show notification
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        ${message}
        <button class="alert-close" onclick="this.parentElement.style.display='none';">&times;</button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
}
