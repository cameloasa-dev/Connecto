// frontend/src/hooks/mutations/useCommentMutations.js

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { postService } from "../../services/post.service";

// ❤️ LIKE / UNLIKE
export const useToggleLike = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (postId) => postService.toggleLike(postId),

    onSuccess: (_, postId) => {
      queryClient.invalidateQueries({ queryKey: ["post", postId] });
      queryClient.invalidateQueries({ queryKey: ["feed"] });
      queryClient.invalidateQueries({ queryKey: ["circle"] });
    },
  });
};

// ➕ ADD COMMENT
export const useAddComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ postId, data }) => postService.addComment(postId, data),

    onSuccess: (_, { postId }) => {
      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "approved"],
      });
      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "pending"],
      });
    },
  });
};

// ✔ APPROVE COMMENT
export const useApproveComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ commentId }) => postService.approveComment(commentId),

    onMutate: ({ postId }) => ({ postId }),

    onSuccess: (_, __, context) => {
      const postId = context.postId;

      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "approved"],
      });
      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "pending"],
      });
    },
  });
};

// ❌ DELETE COMMENT
export const useDeleteComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ commentId }) => postService.deleteComment(commentId),

    onSuccess: (_, { postId }) => {
      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "approved"],
      });
      queryClient.invalidateQueries({
        queryKey: ["comments", postId, "pending"],
      });
    },
  });
};
