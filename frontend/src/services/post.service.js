import api from "./api";

const BASE_URL = "/posts";

export const postService = {
  // ============================
  // POSTS
  // ============================

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

  async updatePost(postId, postData) {
    const res = await api.patch(`${BASE_URL}/${postId}`, postData);
    return res.data;
  },

  async deletePost(postId) {
    await api.delete(`${BASE_URL}/${postId}`);
    return { success: true };
  },

  // ============================
  // LIKES
  // ============================

  async toggleLike(postId) {
    const res = await api.post(`${BASE_URL}/${postId}/like`);
    return res.data;
  },

  // ============================
  // COMMENTS
  // ============================

  async addComment(postId, data) {
    const res = await api.post(`${BASE_URL}/${postId}/comments`, data);
    return res.data;
  },

  async deleteComment(commentId) {
    await api.delete(`${BASE_URL}/comments/${commentId}`);
    return { success: true };
  },

  async approveComment(commentId) {
    const res = await api.post(`${BASE_URL}/comments/${commentId}/approve`);
    return res.data;
  },

  async getApprovedComments(postId) {
    const res = await api.get(`${BASE_URL}/${postId}/comments`);
    return res.data;
  },

  async getPendingComments(postId) {
    const res = await api.get(`${BASE_URL}/${postId}/comments/pending`);
    return res.data;
  },
};
