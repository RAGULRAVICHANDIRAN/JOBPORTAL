/**
 * JobPilot AI — Auth Store (Zustand)
 *
 * Manages authentication state, login/register, and user info.
 */

import { create } from 'zustand';
import api from '../services/api';

const useAuthStore = create((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  // Initialize — check for existing token
  initialize: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ isLoading: false, isAuthenticated: false });
      return;
    }

    try {
      const user = await api.get('/auth/me');
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      api.clearTokens();
      set({ isLoading: false, isAuthenticated: false });
    }
  },

  // Register
  register: async (name, email, password) => {
    set({ error: null, isLoading: true });
    try {
      const data = await api.post('/auth/register', { name, email, password });
      api.setTokens(data.access_token, data.refresh_token);
      const user = await api.get('/auth/me');
      set({ user, isAuthenticated: true, isLoading: false });
      return { success: true };
    } catch (err) {
      set({ error: err.message, isLoading: false });
      return { success: false, error: err.message };
    }
  },

  // Login
  login: async (email, password) => {
    set({ error: null, isLoading: true });
    try {
      const data = await api.post('/auth/login', { email, password });
      api.setTokens(data.access_token, data.refresh_token);
      const user = await api.get('/auth/me');
      set({ user, isAuthenticated: true, isLoading: false });
      return { success: true };
    } catch (err) {
      set({ error: err.message, isLoading: false });
      return { success: false, error: err.message };
    }
  },

  // Logout
  logout: () => {
    api.clearTokens();
    set({ user: null, isAuthenticated: false, error: null });
  },

  clearError: () => set({ error: null }),
}));

// Listen for auth:logout event (from API client on token expiry)
window.addEventListener('auth:logout', () => {
  useAuthStore.getState().logout();
});

export default useAuthStore;
