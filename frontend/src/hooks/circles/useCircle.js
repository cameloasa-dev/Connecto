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
    queryKey: ["myCircles"],
    queryFn: () => circleService.getMyCircles(),
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
    select: (circles) => circles.sort((a, b) => a.name.localeCompare(b.name)),
  });
};
