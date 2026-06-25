// frontend/src/components/comments/CommentList.jsx

import PropTypes from "prop-types";
import { CommentItem } from "./CommentItem";
import "./CommentList.css";

export const CommentList = ({ comments, postId, circleId }) => {
  if (!comments || comments.length === 0) {
    return <div className="no-comments">No comments yet</div>;
  }

  return (
    <div className="comment-list">
      {comments.map((comment) => (
        <CommentItem
          key={comment.id}
          comment={comment}
          postId={postId}
          circleId={circleId}
        />
      ))}
    </div>
  );
};

CommentList.propTypes = {
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      author_id: PropTypes.number.isRequired,
      author_username: PropTypes.string.isRequired,
      content: PropTypes.string.isRequired,
      created_at: PropTypes.string.isRequired,
      status: PropTypes.string.isRequired,
    }),
  ).isRequired,

  postId: PropTypes.number.isRequired,
  circleId: PropTypes.number.isRequired,
};
