// frontend/src/services/api.js
import axios from "axios";
import { API_BASE_URL } from "../config/index";

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    if (import.meta.env.DEV) {
      console.log(`🚀 ${config.method.toUpperCase()} ${config.url}`, config.data);
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log("✅ Response:", response.data);
    }
    return response;
  },
  (error) => {
    if (import.meta.env.DEV) {
      console.error("❌ API Error:", error.response?.data || error.message);
    }

    if (error.response?.status === 401) {
      window.location.href = "/login";
    }

    return Promise.reject(
      new Error(error.response?.data?.detail || "Unexpected API error"),
    );
  },
);

export default api;
