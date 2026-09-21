/**
 * JobPilot AI — API Client
 *
 * Axios-based API client with JWT token management, auto-refresh, and error handling.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

class ApiClient {
  constructor() {
    this.baseUrl = API_BASE;
    this.accessToken = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  setTokens(access, refresh) {
    this.accessToken = access;
    this.refreshToken = refresh;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  clearTokens() {
    this.accessToken = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined,
      });

      // Auto-refresh on 401
      if (response.status === 401 && this.refreshToken) {
        const refreshed = await this.tryRefresh();
        if (refreshed) {
          headers['Authorization'] = `Bearer ${this.accessToken}`;
          const retryResponse = await fetch(url, {
            ...options,
            headers,
            body: options.body ? JSON.stringify(options.body) : undefined,
          });
          return this.handleResponse(retryResponse);
        } else {
          this.clearTokens();
          window.dispatchEvent(new CustomEvent('auth:logout'));
          throw new ApiError('Session expired. Please login again.', 401);
        }
      }

      return this.handleResponse(response);
    } catch (error) {
      if (error instanceof ApiError) throw error;
      throw new ApiError('Network error. Please check your connection.', 0);
    }
  }

  async handleResponse(response) {
    const data = await response.json().catch(() => null);

    if (!response.ok) {
      throw new ApiError(
        data?.detail || `Request failed with status ${response.status}`,
        response.status,
        data,
      );
    }

    return data;
  }

  async tryRefresh() {
    try {
      const response = await fetch(`${this.baseUrl}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: this.refreshToken }),
      });

      if (!response.ok) return false;

      const data = await response.json();
      this.setTokens(data.access_token, data.refresh_token);
      return true;
    } catch {
      return false;
    }
  }

  // Convenience methods
  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  post(endpoint, body) {
    return this.request(endpoint, { method: 'POST', body });
  }

  put(endpoint, body) {
    return this.request(endpoint, { method: 'PUT', body });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }

  async uploadFile(endpoint, file, fieldName = 'file') {
    const url = `${this.baseUrl}${endpoint}`;
    const formData = new FormData();
    formData.append(fieldName, file);

    const headers = {};
    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });

    return this.handleResponse(response);
  }
}

export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = 'ApiError';
  }
}

export const api = new ApiClient();
export default api;
