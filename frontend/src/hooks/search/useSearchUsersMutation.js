//frontend/src/hooks/search/useSearchUsersMutation.js
import { useMutation } from "@tanstack/react-query";
import { circleMemberService } from "../../services/circleMember.service";

export const useSearchUsers = () => {
  return useMutation({
    mutationFn: ({ query, circleId }) =>
      circleMemberService.searchUsers(query, circleId),
  });
};
