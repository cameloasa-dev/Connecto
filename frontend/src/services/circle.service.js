import api from "./api";

const BASE_URL = "/circles";

export const circleService = {
  async getMyCircles() {
    const res = await api.get(`${BASE_URL}/my`);
    return res.data;
  },

  async getCircle(circleId) {
    const res = await api.get(`${BASE_URL}/${circleId}`);
    return res.data;
  },

  async createCircle(circleData) {
    const res = await api.post(BASE_URL, circleData);
    return res.data;
  },

  async updateCircle(circleId, circleData) {
    const res = await api.put(`${BASE_URL}/${circleId}`, circleData);
    return res.data;
  },

  async updateCircleName(circleId, name) {
    const res = await api.put(`${BASE_URL}/${circleId}`, { name });
    return res.data;
  },

  async deleteCircle(circleId) {
    const res = await api.delete(`${BASE_URL}/${circleId}`);
    return res.data;
  },
};
