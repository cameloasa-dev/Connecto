// frontend/src/hooks/useCircleMembersQuery.js
import { useQuery } from "@tanstack/react-query";
import { circleMemberService } from "../services/circleMember.service";

export const useCircleMembersQuery = (circleId) => {
  return useQuery({
    queryKey: ["circleMembers", circleId],
    queryFn: () => circleMemberService.getMembers(circleId),
    enabled: !!circleId,
  });
};
