// frontend/src/services/userDashboard.service.js
import api from "./api";

const BASE_URL = "/dashboard";

export const userDashboardService = {
  async getUserDashboardData() {
    const res = await api.get(BASE_URL);
    return res.data;
  },
};
