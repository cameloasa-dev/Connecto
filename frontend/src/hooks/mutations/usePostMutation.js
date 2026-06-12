// frontend/src/hooks/mutations/usePostMutations.js

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { postService } from "../../services/post.service";

export const useCreatePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: postService.createPost,

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["dashboard"],
      });

      queryClient.invalidateQueries({
        queryKey: ["feed"],
      });

      queryClient.invalidateQueries({
        queryKey: ["circle-posts"],
      });
    },
  });
};

export const useDeletePost = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (postId) => postService.deletePost(postId),

    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["dashboard"],
      });

      queryClient.invalidateQueries({
        queryKey: ["feed"],
      });

      queryClient.invalidateQueries({
        queryKey: ["circle-posts"],
      });
    },
  });
};
