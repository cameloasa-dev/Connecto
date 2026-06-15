import { useState } from "react";
import propTypes from "prop-types";
import PostSettingsModal from "./PostSettingsModal";
import PostActions from "./PostActions";
import { useDeletePost } from "../../hooks/mutations/usePostMutations";

const PostCard = ({ post }) => {
  const [isEditing, setIsEditing] = useState(false);
  const { mutateAsync: deletePost } = useDeletePost();

  const handleDelete = async () => {
    if (!window.confirm("Delete post?")) return;
    await deletePost(post.id);
  };

  return (
    <div className="post-card">
      <h4>{post.title}</h4>
      <p>{post.content}</p>

      <PostActions onEdit={() => setIsEditing(true)} onDelete={handleDelete} />

      {isEditing && (
        <PostSettingsModal post={post} onClose={() => setIsEditing(false)} />
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
