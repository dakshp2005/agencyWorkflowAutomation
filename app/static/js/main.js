// Toast notification system
const Toast = {
  container: null,
  init() {
    this.container = document.querySelector('.toast-container');
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },
  show(message, type = 'info', duration = 4000) {
    if (!this.container) this.init();
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    // Simple icon mapping
    const icons = {
      success: '✅',
      error: '❌',
      info: 'ℹ️'
    };
    
    toast.innerHTML = `<div style="display: flex; gap: 0.75rem; align-items: center;">
      <span>${icons[type] || icons.info}</span>
      <span style="flex:1;">${message}</span>
      <button onclick="this.parentElement.parentElement.remove()" style="background:none;border:none;cursor:pointer;">✖</button>
    </div>`;
    
    this.container.appendChild(toast);
    
    setTimeout(() => {
      if (toast.parentElement) {
        toast.style.animation = 'slideIn 0.3s ease-in reverse forwards';
        setTimeout(() => toast.remove(), 300);
      }
    }, duration);
  },
  success(msg) { this.show(msg, 'success'); },
  error(msg) { this.show(msg, 'error'); },
  info(msg) { this.show(msg, 'info'); }
};

// AJAX helper with loading states
async function apiCall(btn, url, method = 'POST', body = null) {
  if (btn) {
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner">⌛</span> Loading...';
    btn.disabled = true;
  }
  
  try {
    const options = {
      method,
      headers: { 'Accept': 'application/json' }
    };
    if (body) {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(body);
    }
    
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (!response.ok) throw new Error(data.error || data.message || 'API Error');
    return data;
    
  } catch (err) {
    Toast.error(err.message);
    throw err;
  } finally {
    if (btn) {
      btn.innerHTML = btn.dataset.originalText;
      btn.disabled = false;
    }
  }
}

function confirmAction(title, message, onConfirm) {
  if (window.confirm(`${title}\n\n${message}`)) {
    onConfirm();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  Toast.init();
  // Auto-dismiss Flash Messages
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => alert.remove(), 5000);
  });
});
