import axios from 'axios';

// Render provides the backend URL via VITE_API_URL. We append /api to it.
const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL + '/api' : 'http://localhost:8000/api'),
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
