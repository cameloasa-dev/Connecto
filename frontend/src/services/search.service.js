// frontend/src/services/search.service.js
import api from "./api";

export const searchService = {
  async search(query) {
    try {
      const response = await api.get(`/search?q=${encodeURIComponent(query)}`);
      return response.data;
    } catch (err) {
      const message = err.message || "Search failed";
      console.error("Search error:", message);
      throw new Error(message);
    }
  },
};

