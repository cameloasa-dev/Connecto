// frontend/src/services/circleMember.service.js
import api from "./api";

export const circleMemberService = {
  // Search users to add to a circle
  async searchUsers(query, circleId) {
    try {
      const response = await api.get(
        `/users/search?query=${query}&circle_id=${circleId}`,
      );
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to search users";
      console.error("Error searching users:", message);
      throw new Error(message);
    }
  },

  // Add member to circle
  async addMember(circleId, userId) {
    try {
      const response = await api.post(`/circles/${circleId}/members`, {
        user_id: userId,
      });
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to add member";
      console.error("Error adding member:", message);
      throw new Error(message);
    }
  },

  // Remove member from circle
  async removeMember(circleId, userId) {
    try {
      const response = await api.delete(
        `/circles/${circleId}/members/${userId}`,
      );
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to remove member";
      console.error("Error removing member:", message);
      throw new Error(message);
    }
  },

  // Update member role
  async updateRole(circleId, userId, role) {
    try {
      const response = await api.put(
        `/circles/${circleId}/members/${userId}/role`,
        { role },
      );
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to update member role";
      console.error("Error updating role:", message);
      throw new Error(message);
    }
  },
};

