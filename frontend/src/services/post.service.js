import api from "./api";

const BASE_URL = "/posts";

export const postService = {
  async getFeed(limit = 20, offset = 0) {
    const res = await api.get(`${BASE_URL}/feed`, {
      params: { limit, offset },
    });
    return res.data;
  },

  async getCirclePosts(circleId, limit = 50, offset = 0) {
    const res = await api.get(`${BASE_URL}/circle/${circleId}`, {
      params: { limit, offset },
    });
    return res.data;
  },

  async createPost(postData) {
    const res = await api.post(BASE_URL, postData);
    return res.data;
  },

  async getPost(postId) {
    const res = await api.get(`${BASE_URL}/${postId}`);
    return res.data;
  },

  async deletePost(postId) {
    await api.delete(`${BASE_URL}/${postId}`);
    return { success: true };
  },
};
