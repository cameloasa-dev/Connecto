import { useState } from "react";
import propTypes from "prop-types";
import { useCreatePost } from "../../hooks/mutations/usePostMutations";

const CreatePost = ({ onPostCreated, circles = [] }) => {
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    circle_id: null,
  });

  const { mutate, isPending, error } = useCreatePost();

  const resetForm = () => {
    setFormData({
      title: "",
      content: "",
      circle_id: null,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    mutate(formData, {
      onSuccess: (newPost) => {
        onPostCreated(newPost);
        resetForm();
      },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="create-post-form">
      <h3>Create New Post</h3>

      {error && (
        <div className="error-message">
          {error?.response?.data?.detail || "Failed to create post"}
        </div>
      )}

      <div className="form-group">
        <input
          type="text"
          placeholder="Post title"
          value={formData.title}
          onChange={(e) =>
            setFormData({ ...formData, title: e.target.value })
          }
          required
          disabled={isPending}
        />
      </div>

      <div className="form-group">
        <textarea
          placeholder="What's on your mind?"
          value={formData.content}
          onChange={(e) =>
            setFormData({ ...formData, content: e.target.value })
          }
          required
          rows="4"
          disabled={isPending}
        />
      </div>

      <div className="form-group">
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
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? "Posting..." : "Post"}
      </button>
    </form>
  );
};

CreatePost.propTypes = {
  onPostCreated: propTypes.func.isRequired,
  circles: propTypes.arrayOf(
    propTypes.shape({
      id: propTypes.number.isRequired,
      name: propTypes.string.isRequired,
    })
  ),
};

CreatePost.defaultProps = {
  circles: [],
};

export default CreatePost;