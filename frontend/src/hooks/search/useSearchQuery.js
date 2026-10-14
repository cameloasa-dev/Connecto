// frontend/src/hooks/useSearchQuery.js
import { useQuery } from "@tanstack/react-query";
import { searchService } from "../../services/search.service";

export const useSearchQuery = (query, page = 1) => {
  return useQuery({
    queryKey: ["search", query, page],
    queryFn: () => searchService.searchGlobal(query, page),
    enabled: !!query?.trim(),
    staleTime: 1000 * 30, // 30 sec cache
    keepPreviousData: true,
  });
};
