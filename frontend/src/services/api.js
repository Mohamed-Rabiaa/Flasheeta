import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  withCredentials: true, // Important for session-based auth
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add CSRF token if available
api.interceptors.request.use(
  (config) => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.data);
      
      // Handle 401 Unauthorized - redirect to login
      if (error.response.status === 401) {
        window.location.href = '/login';
      }
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
