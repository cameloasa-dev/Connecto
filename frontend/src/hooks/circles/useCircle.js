// frontend/src/hooks/circles/useCircle.js
import { useQuery } from "@tanstack/react-query";
import { circleService } from "../../services/circle.service";

export const useCircle = (circleId) => {
  return useQuery({
    queryKey: ["circle", circleId],
    queryFn: () => circleService.getCircle(circleId),
    enabled: !!circleId,
  });
};

export const useCircles = () => {
  return useQuery({
    queryKey: ["circles"],
    queryFn: () => circleService.getMyCircles(),
  });
};
