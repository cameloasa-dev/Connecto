import { describe, it, expect, vi, beforeEach } from "vitest";
import { postService } from "../../src/services/post.service.js";

// Mock ONLY api layer
vi.mock("../../src/services/api", () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn(),
  },
}));

import api from "../../src/services/api";

describe("postService (unit)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // =========================
  // GET FEED
  // =========================
  describe("getFeed", () => {
    it("fetches feed with params", async () => {
      api.get.mockResolvedValue({
        data: [{ id: 1, content: "post 1" }],
      });

      const result = await postService.getFeed(10, 5);

      expect(api.get).toHaveBeenCalledWith("/posts/feed", {
        params: {
          limit: 10,
          offset: 5,
        },
      });

      expect(result).toEqual([{ id: 1, content: "post 1" }]);
    });
  });

  // =========================
  // GET CIRCLE POSTS
  // =========================
  describe("getCirclePosts", () => {
    it("fetches circle posts with params", async () => {
      api.get.mockResolvedValue({
        data: [{ id: 1, content: "circle post" }],
      });

      const result = await postService.getCirclePosts(1, 20, 0);

      expect(api.get).toHaveBeenCalledWith("/posts/circle/1", {
        params: {
          limit: 20,
          offset: 0,
        },
      });

      expect(result).toEqual([{ id: 1, content: "circle post" }]);
    });
  });

  // =========================
  // CREATE POST
  // =========================
  describe("createPost", () => {
    it("creates a post", async () => {
      const payload = { content: "Hello world" };

      api.post.mockResolvedValue({
        data: { id: 1, content: "Hello world" },
      });

      const result = await postService.createPost(payload);

      expect(api.post).toHaveBeenCalledWith("/posts", payload);
      expect(result).toEqual({ id: 1, content: "Hello world" });
    });
  });

  // =========================
  // GET POST
  // =========================
  describe("getPost", () => {
    it("fetches single post", async () => {
      api.get.mockResolvedValue({
        data: { id: 1, content: "single post" },
      });

      const result = await postService.getPost(1);

      expect(api.get).toHaveBeenCalledWith("/posts/1");
      expect(result).toEqual({ id: 1, content: "single post" });
    });
  });

  // =========================
  // DELETE POST
  // =========================
  describe("deletePost", () => {
    it("deletes post and returns success", async () => {
      api.delete.mockResolvedValue({});

      const result = await postService.deletePost(1);

      expect(api.delete).toHaveBeenCalledWith("/posts/1");
      expect(result).toEqual({ success: true });
    });
  });
});
