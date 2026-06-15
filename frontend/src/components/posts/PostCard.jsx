//frontend/src/components/post/PostCard
import { useState } from "react";
import propTypes from "prop-types";
import PostEditor from "./PostEditor";
import { useDeletePost } from "../../hooks/mutations/usePostMutations";
import "./PostCard.css";

const PostCard = ({ post }) => {
  const [isEditing, setIsEditing] = useState(false);
  const { mutateAsync: deletePost, isPending } = useDeletePost();

  const handleDelete = async () => {
    if (isPending) return;
    if (!window.confirm("Delete post?")) return;

    await deletePost(post.id);
  };

  const closeEditor = () => setIsEditing(false);

  return (
    <div className="post-card">
      <h4>{post.title}</h4>
      <p>{post.content}</p>

      <div className="post-actions">
        <button
          className="post-action-btn"
          onClick={() => setIsEditing(true)}
          disabled={isPending}
        >
          Edit
        </button>

        <button
          className="post-action-btn danger"
          onClick={handleDelete}
          disabled={isPending}
        >
          {isPending ? "Deleting..." : "Delete"}
        </button>
      </div>

      {isEditing && (
        <div className="post-editor-overlay">
          <div className="post-editor-modal">
            <h3>Edit Post</h3>

            <PostEditor
              post={post}
              onSuccess={closeEditor}
              onCancel={closeEditor}
            />
          </div>
        </div>
      )}
    </div>
  );
};

PostCard.propTypes = {
  post: propTypes.shape({
    id: propTypes.number.isRequired,
    title: propTypes.string.isRequired,
    content: propTypes.string.isRequired,
  }).isRequired,
};

export default PostCard;
