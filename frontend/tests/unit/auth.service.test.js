//frontend/tests/unit/auth.service.test.js
import { describe, it, expect, vi, beforeEach } from "vitest";
import { authService } from "../../src/services/auth.service.js";

// Mock ONLY the api layer
vi.mock("../../src/services/api", () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}));

import api from "../../src/services/api";

describe("authService (unit)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // =========================
  // LOGIN
  // =========================
  describe("login", () => {
    it("returns data on success", async () => {
      api.post.mockResolvedValue({
        data: { user: { id: 1, username: "test" } },
      });

      const result = await authService.login({
        username: "test",
        password: "123",
      });

      expect(api.post).toHaveBeenCalledWith("/auth/login", {
        username: "test",
        password: "123",
      });

      expect(result).toEqual({ user: { id: 1, username: "test" } });
    });

    it("throws error on failure", async () => {
      api.post.mockRejectedValue(new Error("Login failed"));

      await expect(
        authService.login({
          username: "wrong",
          password: "wrong",
        }),
      ).rejects.toThrow("Login failed");
    });
  });

  // =========================
  // REGISTER
  // =========================
  describe("register", () => {
    it("sends correct payload and returns data", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await authService.register({
        username: "newuser",
        password: "123",
        email: "test@test.com",
      });

      expect(api.post).toHaveBeenCalledWith("/auth/register", {
        username: "newuser",
        password: "123",
        full_name: "",
        email: "test@test.com",
      });

      expect(result).toEqual({ success: true });
    });
  });

  // =========================
  // LOGOUT
  // =========================
  describe("logout", () => {
    it("returns success on success", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await authService.logout();

      expect(api.post).toHaveBeenCalledWith("/auth/logout");
      expect(result).toEqual({ success: true });
    });

    it("returns fallback object on error", async () => {
      api.post.mockRejectedValue(new Error("fail"));

      const result = await authService.logout();

      expect(result).toEqual({ success: true });
    });
  });

  // =========================
  // CHECK AUTH
  // =========================
  describe("checkAuth", () => {
    it("returns authenticated user", async () => {
      api.get.mockResolvedValue({
        data: { id: 1, username: "test" },
      });

      const result = await authService.checkAuth();

      expect(api.get).toHaveBeenCalledWith("/auth/me");

      expect(result).toEqual({
        authenticated: true,
        user: { id: 1, username: "test" },
      });
    });

    it("returns unauthenticated on error", async () => {
      api.get.mockRejectedValue({
        response: { status: 401 },
      });

      const result = await authService.checkAuth();

      expect(result).toEqual({
        authenticated: false,
        user: null,
      });
    });
  });

  // =========================
  // PASSWORD RESET
  // =========================
  describe("password reset", () => {
    it("requestPasswordReset sends email", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await authService.requestPasswordReset({
        email: "test@test.com",
      });

      expect(api.post).toHaveBeenCalledWith("/auth/reset-password", {
        email: "test@test.com",
      });

      expect(result).toEqual({ success: true });
    });

    it("resetPassword sends token + new password", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await authService.resetPassword({
        token: "abc",
        new_password: "123",
      });

      expect(api.post).toHaveBeenCalledWith("/auth/reset-password/confirm", {
        token: "abc",
        new_password: "123",
      });

      expect(result).toEqual({ success: true });
    });
  });

  // =========================
  // EMAIL VERIFICATION
  // =========================
  describe("email verification", () => {
    it("verifyEmail sends token", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await authService.verifyEmail({
        token: "token123",
      });

      expect(api.post).toHaveBeenCalledWith("/auth/verify-email", {
        token: "token123",
      });

      expect(result).toEqual({ success: true });
    });

    it("resendVerificationEmail sends email", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await authService.resendVerificationEmail({
        email: "test@test.com",
      });

      expect(api.post).toHaveBeenCalledWith("/auth/resend-verification", {
        email: "test@test.com",
      });

      expect(result).toEqual({ success: true });
    });
  });
});
