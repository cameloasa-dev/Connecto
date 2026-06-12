// frontend/src/hooks/mutations/useCircleMutations.js

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { circleService } from "../../services/circle.service";

export const useCreateCircle = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (circleData) => circleService.createCircle(circleData),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["myCircles"],
      });

      queryClient.invalidateQueries({
        queryKey: ["dashboard"],
      });
    },
  });
};

export const useUpdateCircleName = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ circleId, name }) =>
      circleService.updateCircleName(circleId, name),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["circle"],
      });

      queryClient.invalidateQueries({
        queryKey: ["myCircles"],
      });

      queryClient.invalidateQueries({
        queryKey: ["dashboard"],
      });
    },
  });
};
