// frontend/src/hooks/profile/useUserProfileQuery.js
import { useQuery } from "@tanstack/react-query";
import { fetchUserProfile } from "../../services/profileService";

export function useUserProfileQuery(userId) {
  return useQuery({
    queryKey: ["user-profile", userId],
    queryFn: () => fetchUserProfile(userId),
    enabled: !!userId,
  });
}
