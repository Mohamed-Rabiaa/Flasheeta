import api from './api';

const authService = {
  // Login user
  login: async (email, password) => {
    const response = await api.post('/login', { email, password });
    return response.data;
  },

  // Register new user
  register: async (userData) => {
    const response = await api.post('/register', userData);
    return response.data;
  },

  // Logout user
  logout: async () => {
    const response = await api.post('/logout');
    return response.data;
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },
};

export default authService;
