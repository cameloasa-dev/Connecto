// frontend/src/hooks/mutations/useCommentMutations.js

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { postService } from "../../services/post.service";

export const useToggleLike = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (postId) => postService.toggleLike(postId),

    onSuccess: (_, postId) => {
      queryClient.invalidateQueries({ queryKey: ["post", postId] });
    },
  });
};

export const useAddComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ postId, data }) => postService.addComment(postId, data),

    onSuccess: (_, variables) => {
      const { postId } = variables;

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "approved"],
      });

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "pending"],
      });
    },
  });
};

export const useApproveComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (commentId) => postService.approveComment(commentId),

    onSuccess: (_, commentId, context) => {
      const postId = context?.postId;

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "approved"],
      });

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "pending"],
      });
    },
  });
};

export const useDeleteComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ commentId }) => postService.deleteComment(commentId),

    onSuccess: (_, variables) => {
      const { postId } = variables;

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "approved"],
      });

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "pending"],
      });
    },
  });
};
