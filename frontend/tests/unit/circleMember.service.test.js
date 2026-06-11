import { describe, it, expect, vi, beforeEach } from "vitest";
import { circleMemberService } from "../../src/services/circleMember.service.js";

// Mock ONLY api layer
vi.mock("../../src/services/api", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

import api from "../../src/services/api";

describe("circleMemberService (unit)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // =========================
  // SEARCH USERS
  // =========================
  describe("searchUsers", () => {
    it("returns users list", async () => {
      api.get.mockResolvedValue({
        data: [{ id: 1, username: "john" }],
      });

      const result = await circleMemberService.searchUsers("john", 10);

      expect(api.get).toHaveBeenCalledWith("/users/search", {
        params: {
          query: "john",
          circle_id: 10,
        },
      });

      expect(result).toEqual([{ id: 1, username: "john" }]);
    });
  });

  // =========================
  // ADD MEMBER
  // =========================
  describe("addMember", () => {
    it("adds user to circle", async () => {
      api.post.mockResolvedValue({
        data: { success: true },
      });

      const result = await circleMemberService.addMember(10, 5);

      expect(api.post).toHaveBeenCalledWith("/circles/10/members", {
        user_id: 5,
      });

      expect(result).toEqual({ success: true });
    });
  });

  // =========================
  // REMOVE MEMBER
  // =========================
  describe("removeMember", () => {
    it("removes user from circle", async () => {
      api.delete.mockResolvedValue({
        data: { success: true },
      });

      const result = await circleMemberService.removeMember(10, 5);

      expect(api.delete).toHaveBeenCalledWith("/circles/10/members/5");

      expect(result).toEqual({ success: true });
    });
  });

  // =========================
  // UPDATE ROLE
  // =========================
  describe("updateRole", () => {
    it("updates member role", async () => {
      api.put.mockResolvedValue({
        data: { success: true, role: "admin" },
      });

      const result = await circleMemberService.updateRole(10, 5, "admin");

      expect(api.put).toHaveBeenCalledWith("/circles/10/members/5/role", {
        role: "admin",
      });

      expect(result).toEqual({
        success: true,
        role: "admin",
      });
    });
  });
});
