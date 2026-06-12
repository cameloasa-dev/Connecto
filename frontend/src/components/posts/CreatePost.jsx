import { useState } from "react";
import { useCreatePost } from "../../hooks/useCreatePostMutation";

// eslint-disable-next-line react/prop-types
const CreatePost = ({ onPostCreated, circles = [] }) => {
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    circle_id: null,
  });

  const { mutate, isPending, error } = useCreatePost();

  const handleSubmit = (e) => {
    e.preventDefault();

    mutate(formData, {
      onSuccess: (newPost) => {
        onPostCreated(newPost);
        setFormData({ title: "", content: "", circle_id: null });
      },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="create-post-form">
      <h3>Create New Post</h3>

      {error && <div className="error-message">Failed to create post</div>}

      <div className="form-group">
        <input
          type="text"
          placeholder="Post title"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
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

export default CreatePost;
