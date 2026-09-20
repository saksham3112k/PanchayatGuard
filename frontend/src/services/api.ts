import axios from 'axios';

// In production, the React app is served by FastAPI on the same domain, so we just use '/api'
// In development, we use localhost:8000
const api = axios.create({
  baseURL: import.meta.env.PROD ? '/api' : 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
