//frontend/src/components/posts/PostEditor.jsx
import { useState } from "react";
import PropTypes from "prop-types";
import {
  useCreatePost,
  useUpdatePost,
} from "../../hooks/mutations/usePostMutations";

const PostEditor = ({ post, circles = [], onSuccess, onCancel }) => {
  const isEdit = !!post;

  const [formData, setFormData] = useState({
    title: post?.title || "",
    content: post?.content || "",
    circle_id: post?.circle_id || null,
  });

  const { mutateAsync: createPost, isPending: creating } = useCreatePost();

  const { mutateAsync: updatePost, isPending: updating } = useUpdatePost();

  const isPending = creating || updating;

  const handleSave = async () => {
    try {
      if (isEdit) {
        // EDIT MODE
        await updatePost({
          postId: post.id,
          postData: {
            title: formData.title,
            content: formData.content,
            circle_id: formData.circle_id,
          },
        });
      } else {
        // CREATE MODE
        await createPost(formData);
      }

      onSuccess();
    } catch (err) {
      console.error("Failed to save post:", err);
    }
  };

  return (
    <div className="post-editor">
      <h3>{isEdit ? "Edit Post" : "Create New Post"}</h3>

      <input
        type="text"
        placeholder="Post title"
        value={formData.title}
        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        disabled={isPending}
      />

      <textarea
        placeholder="What's on your mind?"
        value={formData.content}
        onChange={(e) => setFormData({ ...formData, content: e.target.value })}
        rows="4"
        disabled={isPending}
      />

      <select
        value={formData.circle_id || ""}
        onChange={(e) =>
          setFormData({
            ...formData,
            circle_id: e.target.value ? Number(e.target.value) : null,
          })
        }
        disabled={isPending}
      >
        <option value="">Public Post</option>
        {circles.map((circle) => (
          <option key={circle.id} value={circle.id}>
            {circle.name}
          </option>
        ))}
      </select>

      <div className="actions">
        <button
          className="primary-btn"
          onClick={handleSave}
          disabled={isPending}
        >
          {isEdit ? "Save Changes" : "Post"}
        </button>

        <button
          className="secondary-btn"
          onClick={onCancel}
          disabled={isPending}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

PostEditor.propTypes = {
  post: PropTypes.shape({
    id: PropTypes.number,
    title: PropTypes.string,
    content: PropTypes.string,
    circle_id: PropTypes.number,
  }),
  circles: PropTypes.array,
  onSuccess: PropTypes.func.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default PostEditor;
