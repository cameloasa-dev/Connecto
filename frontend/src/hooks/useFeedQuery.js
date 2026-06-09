// frontend/src/hooks/useFeedQuery.js
import { useQuery } from "@tanstack/react-query";
import { postService } from "../services/post.service";

export const useFeedQuery = (limit = 20) => {
  return useQuery({
    queryKey: ["feed", limit],
    queryFn: () => postService.getFeed(limit),
  });
};
