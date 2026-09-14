import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '', // In dev, uses relative URL so proxy catches it
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Network error';
    return Promise.reject(new Error(message));
  }
)

export default apiClient;
