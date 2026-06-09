// frontend/src/hooks/useCircleQuery.js
import { useQuery } from "@tanstack/react-query";
import { circleService } from "../services/circle.service";

export const useCircleQuery = (circleId) => {
  return useQuery({
    queryKey: ["circle", circleId],
    queryFn: () => circleService.getCircleById(circleId),
    enabled: !!circleId,
  });
};
