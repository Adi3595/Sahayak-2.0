// auth.js - Shared authentication handling for all pages

const API_BASE_URL = window.location.hostname.includes('localhost') ||
                     window.location.hostname.includes('127.0.0.1')
    ? 'http://127.0.0.5:8000'
    : 'https://sahayak-2-0.onrender.com';

// Check authentication status
async function checkAuth() {
    const token = localStorage.getItem('sahayak_token');
    const userId = localStorage.getItem('sahayak_user_id');
    
    if (!token || !userId) {
        redirectToLogin();
        return false;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            clearAuth();
            redirectToLogin();
            return false;
        }
        
        const userData = await response.json();
        updateUserUI(userData);
        return true;
    } catch (error) {
        console.error('Auth check failed:', error);
        clearAuth();
        redirectToLogin();
        return false;
    }
}

// Redirect to login page
function redirectToLogin() {
    const currentPage = window.location.pathname;
    const redirectUrl = `/index.html?redirect=${encodeURIComponent(currentPage)}`;
    window.location.href = redirectUrl;
}

// Clear authentication data
function clearAuth() {
    localStorage.removeItem('sahayak_token');
    localStorage.removeItem('sahayak_user_id');
    localStorage.removeItem('sahayak_user_name');
    localStorage.removeItem('sahayak_token_expiry');
}

// Update UI for logged in user
function updateUserUI(userData) {
    // Update user name in sidebar
    const userNameElements = document.querySelectorAll('.user-name, .sidebar-footer .font-semibold');
    userNameElements.forEach(el => {
        if (el) el.textContent = userData.full_name || userData.username;
    });
    
    // Update user email
    const userEmailElements = document.querySelectorAll('.user-email');
    userEmailElements.forEach(el => {
        if (el) el.textContent = userData.email;
    });
    
    // Update avatar
    const avatarElements = document.querySelectorAll('.user-avatar');
    const avatarUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(userData.full_name || userData.username)}&background=7c3aed&color=fff`;
    avatarElements.forEach(el => {
        if (el) el.src = avatarUrl;
    });
    
    // Show/hide appropriate UI elements
    const authButtons = document.querySelectorAll('#authButtonsNav, .auth-buttons');
    authButtons.forEach(el => {
        if (el) el.classList.add('hidden');
    });
    
    const userProfileElements = document.querySelectorAll('#userProfileNav, .user-profile-container');
    userProfileElements.forEach(el => {
        if (el) el.classList.remove('hidden');
    });
}

// Get auth headers for API calls
function getAuthHeaders(contentType = 'application/json') {
    const token = localStorage.getItem('sahayak_token');
    const headers = {
        'Authorization': `Bearer ${token}`
    };
    if (contentType) {
        headers['Content-Type'] = contentType;
    }
    return headers;
}

// Logout function
function logout() {
    clearAuth();
    window.location.href = '/index.html';
}

// Show toast notification
function showToast(message, type = 'info') {
    // Remove existing toast
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) existingToast.remove();
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-notification fixed bottom-4 right-4 z-50 px-6 py-3 rounded-lg shadow-lg transition-all duration-300 transform translate-y-0 ${
        type === 'success' ? 'bg-emerald-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-amber-500' :
        'bg-purple-500'
    } text-white`;
    toast.innerHTML = `
        <div class="flex items-center gap-2">
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Make authenticated API call
async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('sahayak_token');
    
    if (!token) {
        redirectToLogin();
        throw new Error('Not authenticated');
    }
    
    const defaultOptions = {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, mergedOptions);
        
        if (response.status === 401) {
            clearAuth();
            redirectToLogin();
            throw new Error('Session expired. Please login again.');
        }
        
        return response;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Check if user is logged in
function isLoggedIn() {
    const token = localStorage.getItem('sahayak_token');
    return !!token;
}

// Get current user info
async function getCurrentUser() {
    const token = localStorage.getItem('sahayak_token');
    if (!token) return null;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        console.error('Error getting current user:', error);
        return null;
    }
}

// Auto-initialize on page load for protected pages
document.addEventListener('DOMContentLoaded', async () => {
    // List of public pages that don't require authentication
    const publicPages = ['/index.html', '/', '/login.html', '/signup.html'];
    const currentPath = window.location.pathname;
    
    // Skip auth check for public pages
    if (publicPages.includes(currentPath) || currentPath === '/') {
        // Still check if user is logged in to show/hide UI elements
        const token = localStorage.getItem('sahayak_token');
        if (token) {
            try {
                const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.ok) {
                    const userData = await response.json();
                    updateUserUI(userData);
                }
            } catch (error) {
                // Silently fail on public pages
            }
        }
        return;
    }
    
    // For protected pages, check authentication
    const loadingEl = document.getElementById('auth-loading');
    const isAuth = await checkAuth();
    
    if (isAuth && loadingEl) {
        loadingEl.style.display = 'none';
    }
});