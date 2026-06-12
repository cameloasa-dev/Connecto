// frontend/src/hooks/useMyCirclesQuery.js
import { useQuery } from "@tanstack/react-query";
import { circleService } from "../../services/circle.service";

export const useMyCirclesQuery = () => {
  return useQuery({
    queryKey: ["myCircles"],
    queryFn: () => circleService.getMyCircles(),
  });
};
