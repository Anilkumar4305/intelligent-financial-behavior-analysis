import axios from "axios";

/**
 * Central Axios Client
 * All API calls go through this
 */

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Response Interceptor
 * Makes error handling consistent across app
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Something went wrong";

    console.error("API Error:", message);
    return Promise.reject(message);
  }
);

export default api;
