//frontend/tests/unit/auth.service.test.js
import { describe, it, expect, vi, beforeEach } from "vitest";
import { circleService } from "../../src/services/circle.service.js";

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

describe("circleService (unit)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // =========================
  // GET MY CIRCLES
  // =========================
  describe("getMyCircles", () => {
    it("returns circles list", async () => {
      api.get.mockResolvedValue({
        data: [{ id: 1, name: "Circle 1" }],
      });

      const result = await circleService.getMyCircles();

      expect(api.get).toHaveBeenCalledWith("/circles/my");
      expect(result).toEqual([{ id: 1, name: "Circle 1" }]);
    });
  });

  // =========================
  // GET CIRCLE
  // =========================
  describe("getCircle", () => {
    it("returns a single circle", async () => {
      api.get.mockResolvedValue({
        data: { id: 1, name: "Circle 1" },
      });

      const result = await circleService.getCircle(1);

      expect(api.get).toHaveBeenCalledWith("/circles/1");
      expect(result).toEqual({ id: 1, name: "Circle 1" });
    });
  });

  // =========================
  // CREATE CIRCLE
  // =========================
  describe("createCircle", () => {
    it("creates a circle", async () => {
      const payload = { name: "New Circle" };

      api.post.mockResolvedValue({
        data: { id: 1, name: "New Circle" },
      });

      const result = await circleService.createCircle(payload);

      expect(api.post).toHaveBeenCalledWith("/circles", payload);
      expect(result).toEqual({ id: 1, name: "New Circle" });
    });
  });

  // =========================
  // UPDATE CIRCLE
  // =========================
  describe("updateCircle", () => {
    it("updates circle name and description", async () => {
      api.put.mockResolvedValue({
        data: {
          id: 1,
          name: "Updated",
          description: "New description",
        },
      });

      const payload = {
        name: "Updated",
        description: "New description",
      };

      const result = await circleService.updateCircle(1, payload);

      expect(api.put).toHaveBeenCalledWith("/circles/1", payload);

      expect(result).toEqual({
        id: 1,
        name: "Updated",
        description: "New description",
      });
    });
  });

  // =========================
  // DELETE CIRCLE
  // =========================
  describe("deleteCircle", () => {
    it("deletes a circle", async () => {
      api.delete.mockResolvedValue({
        data: { success: true },
      });

      const result = await circleService.deleteCircle(1);

      expect(api.delete).toHaveBeenCalledWith("/circles/1");
      expect(result).toEqual({ success: true });
    });
  });
});
