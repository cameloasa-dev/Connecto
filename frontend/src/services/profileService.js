// frontend/src/services/profileService.js
import api from "./api";

export async function fetchUserProfile(userId) {
  const response = await api.get(`/users/${userId}/profile`);
  return response.data;
}
