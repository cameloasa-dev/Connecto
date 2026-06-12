//frontend/src/components/posts/PostSettings.jsx
import { useState } from "react";
import propTypes from "prop-types";
import { useUpdatePost } from "../../hooks/mutations/usePostMutations";
import "./PostSettings.css";

const PostSettings = ({ post }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(post.title);
  const [content, setContent] = useState(post.content);

  const { mutateAsync: updatePost, isPending } = useUpdatePost();

  const handleSave = async () => {
    if (title === post.title && content === post.content) {
      setIsEditing(false);
      return;
    }

    await updatePost({
      postId: post.id,
      data: { title, content },
    });

    setIsEditing(false);
  };

  if (!isEditing) {
    return (
      <div>
        <button onClick={() => setIsEditing(true)}>Edit</button>
      </div>
    );
  }

  return (
    <div className="post-settings">
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea value={content} onChange={(e) => setContent(e.target.value)} />

      <button onClick={handleSave} disabled={isPending}>
        Save
      </button>

      <button onClick={() => setIsEditing(false)} disabled={isPending}>
        Cancel
      </button>
    </div>
  );
};

PostSettings.propTypes = {
  post: propTypes.shape({
    id: propTypes.string.isRequired,    
    title: propTypes.string.isRequired,
    content: propTypes.string.isRequired,
  }).isRequired,
};

export default PostSettings;