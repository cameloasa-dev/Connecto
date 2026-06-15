// frontend/src/hooks/useSearchQuery.js
import { useQuery } from "@tanstack/react-query";
import { searchService } from "../../services/search.service";

export const useSearchQuery = (query) => {
  return useQuery({
    queryKey: ["search", "global", query],
    queryFn: () => searchService.searchGlobal(query),
    enabled: !!query?.trim(), 
  });
};
