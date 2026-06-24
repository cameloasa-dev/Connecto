//frontend/src/components/post/PostCard
import { useState } from "react";
import propTypes from "prop-types";
import PostEditor from "./PostEditor";
import { useDeletePost } from "../../hooks/mutations/usePostMutations";
import "./PostCard.css";

const PostCard = ({ post, circles }) => {
  const [isEditing, setIsEditing] = useState(false);
  const { mutateAsync: deletePost, isPending } = useDeletePost();

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (isPending) return;
    if (!window.confirm("Delete post?")) return;

    await deletePost(post.id);
  };

  const closeEditor = () => setIsEditing(false);

  return (
    <>
      {/* CARD */}
      <div className="post-card">
        <div className="post-content">
          <h4>{post.title}</h4>
          <p>{post.content}</p>
        </div>

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
      </div>

      {/* EDITOR MODAL — OUTSIDE CARD */}
      {isEditing && (
        <div className="post-editor-overlay">
          <div className="post-editor-modal">
            <PostEditor
              post={post}
              circles={circles}   
              onSuccess={closeEditor}
              onCancel={closeEditor}
            />
          </div>
        </div>
      )}
    </>
  );
};

PostCard.propTypes = {
  post: propTypes.shape({
    id: propTypes.number.isRequired,
    title: propTypes.string.isRequired,
    content: propTypes.string.isRequired,
    circle_id: propTypes.number,
  }).isRequired,

  circles: propTypes.arrayOf(
    propTypes.shape({
      id: propTypes.number.isRequired,
      name: propTypes.string.isRequired,
    })
  ).isRequired,
};

export default PostCard;

