//src/service/SearchService
import api from "./api";

const BASE_URL = "/search";

export const searchService = {
  async searchGlobal(query) {
    const res = await api.get(BASE_URL, {
      params: {
        q: query,
      },
    });

    return res.data;
  },
};
