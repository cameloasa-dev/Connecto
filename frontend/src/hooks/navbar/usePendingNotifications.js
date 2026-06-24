import { useQuery } from "@tanstack/react-query";
import { circleService } from "../../services/circle.service";

export const usePendingNotifications = () => {
  return useQuery({
    queryKey: ["pending-notifications"],

    queryFn: async () => {
      // 1. all de circles where user is
      const circles = await circleService.getMyCircles();

      // 2. Filter after owner or moderator
      const moderatedCircles = circles.filter(
        (c) => c.role === "owner" || c.role === "moderator",
      );

      // 3. For every circle map pending
      const pendingData = await Promise.all(
        moderatedCircles.map(async (circle) => {
          const pending = await circleService.getPendingComments(circle.id);
          return {
            circleId: circle.id,
            circleName: circle.name,
            comments: pending,
          };
        }),
      );

      // 4. Total
      const total = pendingData.reduce((sum, c) => sum + c.comments.length, 0);

      return {
        total,
        circles: pendingData,
      };
    },

    staleTime: 10_000, // 10 secunds
    refetchInterval: 15_000, // auto-refresh
  });
};
