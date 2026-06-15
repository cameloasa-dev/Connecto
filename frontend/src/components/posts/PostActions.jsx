//frontend/src/components/posts/PostActions.jsx
import React from "react";
import propTypes from "prop-types";

const PostActions = ({ onLike, onComment, onShare }) => {
  return (
    <div className="post-actions">
      <button className="post-action-btn" onClick={onLike}>
        ❤️ Like
      </button>

      <button className="post-action-btn" onClick={onComment}>
        💬 Comment
      </button>

      <button className="post-action-btn" onClick={onShare}>
        🔄 Share
      </button>
    </div>
  );
};

PostActions.propTypes = {
  onLike: propTypes.func,
  onComment: propTypes.func,
  onShare: propTypes.func,
};

PostActions.defaultProps = {
  onLike: () => {},
  onComment: () => {},
  onShare: () => {},
};

export default PostActions;
