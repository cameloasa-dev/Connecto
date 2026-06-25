// frontend/src/components/comments/CommentForm.jsx

import { useState } from "react";
import PropTypes from "prop-types";
import { useAddComment } from "../../hooks/mutations/useCommentMutations";
import "./CommentForm.css";

export const CommentForm = ({ postId }) => {
  const [content, setContent] = useState("");
  const [error, setError] = useState("");

  const addComment = useAddComment();

  const handleSubmit = (e) => {
    e.preventDefault();

    if (content.trim().length === 0) {
      setError("Comment cannot be empty");
      return;
    }

    setError("");

    addComment.mutate(
      {
        postId,
        data: { content },
      },
      {
        onSuccess: () => {
          setContent("");
        },
      },
    );
  };

  return (
    <form className="comment-form" onSubmit={handleSubmit}>
      <textarea
        className="comment-textarea"
        placeholder="Write a comment..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      {error && <div className="comment-error">{error}</div>}

      <button
        className="comment-submit"
        type="submit"
        disabled={addComment.isPending}
      >
        {addComment.isPending ? "Posting..." : "Post Comment"}
      </button>
    </form>
  );
};

CommentForm.propTypes = {
  postId: PropTypes.number.isRequired,
};
