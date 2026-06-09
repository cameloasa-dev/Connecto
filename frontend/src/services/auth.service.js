// frontend/src/services/auth.service.js
import api from "./api";

export const authService = {
  async login({ username, password }) {
    try {
      const response = await api.post("/auth/login", {
        username,
        password,
      });
      return response.data;
    } catch (err) {
      const message = err.message || "Login failed";
      console.error("Login error:", message);
      throw new Error(message);
    }
  },

  async register({ username, password, full_name = "", email = "" }) {
    try {
      const response = await api.post("/auth/register", {
        username,
        password,
        full_name,
        email,
      });
      return response.data;
    } catch (err) {
      const message = err.message || "Registration failed";
      console.error("Register error:", message);
      throw new Error(message);
    }
  },

  async logout() {
    try {
      const response = await api.post("/auth/logout");
      return response.data;
    } catch (err) {
      console.warn("Logout error:", err.message);
      return { success: true };
    }
  },

  async requestPasswordReset({ email }) {
    try {
      const response = await api.post("/auth/reset-password", { email });
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to request password reset";
      console.error("Password reset request error:", message);
      throw new Error(message);
    }
  },

  async resetPassword({ token, new_password }) {
    try {
      const response = await api.post("/auth/reset-password/confirm", {
        token,
        new_password,
      });
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to reset password";
      console.error("Password reset error:", message);
      throw new Error(message);
    }
  },

  async verifyEmail({ token }) {
    try {
      const response = await api.post("/auth/verify-email", { token });
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to verify email";
      console.error("Email verification error:", message);
      throw new Error(message);
    }
  },

  async resendVerificationEmail({ email }) {
    try {
      const response = await api.post("/auth/resend-verification", { email });
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to resend verification email";
      console.error("Resend verification error:", message);
      throw new Error(message);
    }
  },

  async checkAuth() {
    try {
      const response = await api.get("/auth/me");
      return {
        authenticated: true,
        user: response.data,
      };
    } catch (err) {
      if (err.cause?.response?.status === 401) {
        return { authenticated: false, user: null };
      }
      console.warn("Auth check failed:", err.message);
      return { authenticated: false, user: null };
    }
  },
};
