// frontend/src/services/post.service.js
import api from "./api";

const BASE_URL = "/posts";

export const postService = {
  // Get feed (recent posts from user's circles)
  async getFeed(limit = 20, offset = 0) {
    try {
      const response = await api.get(
        `${BASE_URL}/feed?limit=${limit}&offset=${offset}`,
      );
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to fetch feed";
      console.error("Error fetching feed:", message);
      throw new Error(message);
    }
  },

  // Get posts from a specific circle
  async getCirclePosts(circleId, limit = 50, offset = 0) {
    try {
      const response = await api.get(
        `${BASE_URL}/circle/${circleId}?limit=${limit}&offset=${offset}`,
      );
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to fetch circle posts";
      console.error("Error fetching circle posts:", message);
      throw new Error(message);
    }
  },

  // Create post
  async createPost(postData) {
    try {
      const response = await api.post(BASE_URL, postData);
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to create post";
      console.error("Error creating post:", message);
      throw new Error(message);
    }
  },

  // Get single post
  async getPost(postId) {
    try {
      const response = await api.get(`${BASE_URL}/${postId}`);
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to fetch post";
      console.error("Error fetching post:", message);
      throw new Error(message);
    }
  },

  // Delete post
  async deletePost(postId) {
    try {
      await api.delete(`${BASE_URL}/${postId}`);
      return { success: true };
    } catch (err) {
      const message = err.message || "Failed to delete post";
      console.error("Error deleting post:", message);
      throw new Error(message);
    }
  },
};
