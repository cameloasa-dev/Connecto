// frontend/src/hooks/posts/useCirclePosts.js
import { useQuery } from "@tanstack/react-query";
import { postService } from "../../services/post.service";

export const useCirclePosts = (circleId) => {
  return useQuery({
    queryKey: ["circle-posts", circleId],
    queryFn: () => postService.getCirclePosts(circleId),
    enabled: !!circleId,
  });
};

export const usePost = (postId) => {
  return useQuery({
    queryKey: ["post", postId],
    queryFn: () => postService.getPost(postId),
    enabled: !!postId,
  });
};
