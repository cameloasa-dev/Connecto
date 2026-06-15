import api from "./api";

export const searchService = {
  async searchGlobal(query) {
    const res = await api.get("/search", {
      params: {
        q: query,
      },
    });
    return res.data;
  },
};
