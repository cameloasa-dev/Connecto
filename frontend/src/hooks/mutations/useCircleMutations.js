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

export const useUpdateCircle = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ circleId, circleData }) =>
      circleService.updateCircle(circleId, circleData),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["circle", variables.circleId],
      });
      queryClient.invalidateQueries({ queryKey: ["myCircles"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
};

export const useDeleteCircle = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (circleId) => circleService.deleteCircle(circleId),

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
