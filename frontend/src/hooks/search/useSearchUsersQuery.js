//frontend/src/hooks/search/useSearchUsersQuery.js
import { useQuery } from "@tanstack/react-query";
import { circleMemberService } from "../../services/circleMember.service";

export const useSearchUsersQuery = (query, circleId) => {
  return useQuery({
    queryKey: ["user-search", circleId, query],
    queryFn: () => circleMemberService.searchUsers(query, circleId),
    enabled: !!query && query.length > 2,
  });
};
