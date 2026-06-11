// frontend/src/services/auth.service.js
import api from "./api";

export const authService = {
  async login({ username, password }) {
    const { data } = await api.post("/auth/login", {
      username,
      password,
    });

    return data;
  },

  async register({ username, password, full_name = "", email = "" }) {
    const { data } = await api.post("/auth/register", {
      username,
      password,
      full_name,
      email,
    });

    return data;
  },

  async logout() {
    try {
      const { data } = await api.post("/auth/logout");
      return data;
    } catch {
      return { success: true };
    }
  },

  async requestPasswordReset({ email }) {
    const { data } = await api.post("/auth/reset-password", { email });
    return data;
  },

  async resetPassword({ token, new_password }) {
    const { data } = await api.post("/auth/reset-password/confirm", {
      token,
      new_password,
    });

    return data;
  },

  async verifyEmail({ token }) {
    const { data } = await api.post("/auth/verify-email", { token });
    return data;
  },

  async resendVerificationEmail({ email }) {
    const { data } = await api.post("/auth/resend-verification", { email });
    return data;
  },

  async checkAuth() {
    try {
      const { data } = await api.get("/auth/me");

      return {
        authenticated: true,
        user: data,
      };
    } catch (err) {
      const status = err.response?.status;

      if (status === 401) {
        return {
          authenticated: false,
          user: null,
        };
      }

      console.warn("Auth check failed:", err.message);

      return {
        authenticated: false,
        user: null,
      };
    }
  },
};
