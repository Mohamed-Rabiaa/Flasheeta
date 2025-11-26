import api from './api';

const authService = {
  // Login user
  login: async (email, password) => {
    const response = await api.post('/login', { email, password });
    // Store JWT token in localStorage
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    // Return user object (not the full response)
    return response.data.user;
  },

  // Register new user
  register: async (userData) => {
    const response = await api.post('/register', userData);
    // Store JWT token in localStorage
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    // Return user object (not the full response)
    return response.data.user;
  },

  // Logout user
  logout: async () => {
    try {
      await api.post('/logout');
    } catch (error) {
      // Continue with logout even if API call fails
      console.warn('Logout API call failed:', error);
    } finally {
      // Always remove token from localStorage
      localStorage.removeItem('access_token');
    }
    return { message: 'Logged out successfully' };
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },

  // Check if user has valid token
  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};

export default authService;
