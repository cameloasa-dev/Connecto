// frontend/src/components/comments/CommentItem.jsx

import PropTypes from "prop-types";
import { useAuth } from "../../contexts/useAuth";
import {
  useDeleteComment,
  useApproveComment,
} from "../../hooks/mutations/useCommentMutations";
import { useCirclePermissions } from "../../hooks/circles/useCirclePermissions";
import "./CommentItem.css";

export const CommentItem = ({ comment, postId, circleId }) => {
  const { user } = useAuth();

  const { isModerator } = useCirclePermissions(circleId);

  const deleteMutation = useDeleteComment();
  const approveMutation = useApproveComment();

  const isAuthor = user?.id === comment.author_id;

  const handleDelete = () => {
    deleteMutation.mutate({
      commentId: comment.id,
      postId,
    });
  };

  const handleApprove = () => {
    approveMutation.mutate({
      commentId: comment.id,
      postId,
    });
  };

  return (
    <div className="comment-item">
      <div className="comment-header">
        <span className="comment-author">@{comment.author_username}</span>
        <span className="comment-date">
          {new Date(comment.created_at).toLocaleString()}
        </span>
      </div>

      <div className="comment-content">{comment.content}</div>

      <div className="comment-actions">
        {(isAuthor || isModerator) && (
          <button className="comment-btn delete" onClick={handleDelete}>
            Delete
          </button>
        )}

        {isModerator && comment.status === "pending" && (
          <button className="comment-btn approve" onClick={handleApprove}>
            Approve
          </button>
        )}
      </div>
    </div>
  );
};

CommentItem.propTypes = {
  comment: PropTypes.shape({
    id: PropTypes.number.isRequired,
    author_id: PropTypes.number.isRequired,
    author_username: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
    created_at: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired, // "approved" | "pending"
  }).isRequired,

  postId: PropTypes.number.isRequired,
  circleId: PropTypes.number.isRequired,
};
