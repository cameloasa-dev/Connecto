// frontend/src/hooks/mutations/useCircleMemberMutations.js
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { circleMemberService } from "../../services/circleMember.service";

/**
 * ADD MEMBER
 */
export const useAddCircleMember = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ circleId, userId }) =>
      circleMemberService.addMember(circleId, userId),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["circle", variables.circleId],
      });
    },
  });
};

/**
 * REMOVE MEMBER
 */
export const useRemoveCircleMember = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ circleId, userId }) =>
      circleMemberService.removeMember(circleId, userId),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["circle", variables.circleId],
      });
    },
  });
};

/**
 * UPDATE MEMBER ROLE
 */
export const useUpdateCircleMemberRole = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ circleId, userId, role }) =>
      circleMemberService.updateMemberRole(circleId, userId, role),

    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["circle", variables.circleId],
      });
    },
  });
};
