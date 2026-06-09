// frontend/src/services/circle.service.js
import api from "./api";

const BASE_URL = "/circles";

export const circleService = {
  // Get all circles where the user is a member
  async getMyCircles() {
    try {
      const response = await api.get(`${BASE_URL}/my`);
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to fetch circles";
      console.error("Error fetching circles:", message);
      throw new Error(message);
    }
  },

  // Get a specific circle by ID
  async getCircle(circleId) {
    try {
      const response = await api.get(`${BASE_URL}/${circleId}`);
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to fetch circle";
      console.error("Error fetching circle:", message);
      throw new Error(message);
    }
  },

  // Create a new circle
  async createCircle(circleData) {
    try {
      const response = await api.post(BASE_URL, circleData);
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to create circle";
      console.error("Error creating circle:", message);
      throw new Error(message);
    }
  },

  // Update circle name (owner only)
  async updateCircleName(circleId, name) {
    try {
      const response = await api.put(`${BASE_URL}/${circleId}/name`, { name });
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to update circle name";
      console.error("Error updating circle name:", message);
      throw new Error(message);
    }
  },

  // Delete a circle (owner only)
  async deleteCircle(circleId) {
    try {
      const response = await api.delete(`${BASE_URL}/${circleId}`);
      return response.data;
    } catch (err) {
      const message = err.message || "Failed to delete circle";
      console.error("Error deleting circle:", message);
      throw new Error(message);
    }
  },
};
