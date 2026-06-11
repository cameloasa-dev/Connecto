import api from "./api";

export const circleMemberService = {
  async searchUsers(query, circleId) {
    const res = await api.get("/users/search", {
      params: {
        query,
        circle_id: circleId,
      },
    });
    return res.data;
  },

  async addMember(circleId, userId) {
    const res = await api.post(`/circles/${circleId}/members`, {
      user_id: userId,
    });
    return res.data;
  },

  async removeMember(circleId, userId) {
    const res = await api.delete(`/circles/${circleId}/members/${userId}`);
    return res.data;
  },

  async updateRole(circleId, userId, role) {
    const res = await api.put(`/circles/${circleId}/members/${userId}/role`, {
      role,
    });
    return res.data;
  },
};
