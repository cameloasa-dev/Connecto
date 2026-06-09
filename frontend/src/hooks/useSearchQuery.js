// frontend/src/hooks/useSearchQuery.js
import { useQuery } from "@tanstack/react-query";
import { searchService } from "../services/search.service";

export const useSearchQuery = (query) => {
  return useQuery({
    queryKey: ["search", query],
    queryFn: () => searchService.search(query),
    enabled: query.length > 0, // Only run the query if the search query is not empty   
  });
};
