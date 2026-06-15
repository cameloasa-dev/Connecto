//frontend/src/components/posts/PostEditor.jsx
import { useState } from "react";
import propTypes from "prop-types";
import { useUpdatePost } from "../../hooks/mutations/usePostMutations";

const PostEditor = ({ post, onSuccess, onCancel }) => {
  const [title, setTitle] = useState(post.title);
  const [content, setContent] = useState(post.content);

  const { mutateAsync: updatePost, isPending } = useUpdatePost();

  const handleSave = async () => {
    try {
      if (title === post.title && content === post.content) {
        onCancel();
        return;
      }

      await updatePost({
        postId: post.id,
        postData: { title, content },
      });

      onSuccess();
    } catch (err) {
      console.error("Failed to update post:", err);
    }
  };
  return (
    <div className="post-editor">
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        disabled={isPending}
      />

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        disabled={isPending}
      />

      <div className="actions">
        <button onClick={handleSave} disabled={isPending}>
          Save
        </button>

        <button onClick={onCancel} disabled={isPending}>
          Cancel
        </button>
      </div>
    </div>
  );
};

PostEditor.propTypes = {
  post: propTypes.shape({
    id: propTypes.number.isRequired,
    title: propTypes.string.isRequired,
    content: propTypes.string.isRequired,
  }).isRequired,
  onSuccess: propTypes.func.isRequired,
  onCancel: propTypes.func.isRequired,
};

export default PostEditor;
