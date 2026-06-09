// frontend/src/services/search.service.js
import api from "./api";

export const searchService = {
  async search(query) {
    try {
      const response = await api.get(`/users?limit=100`);
      const allUsers = response.data || [];

      const filteredUsers = allUsers.filter((user) =>
        user.username.toLowerCase().includes(query.toLowerCase()),
      );

      return {
        users: filteredUsers,
        circles: [],
        posts: [],
      };
    } catch (err) {
      const message = err.message || "Search failed";
      console.error("Search error:", message);
      return { users: [], circles: [], posts: [] };
    }
  },
};

