// frontend/src/components/layout/CreatePost.jsx
import { useState } from "react";
import { postService } from "../../services/post.service";

const CreatePost = ({ onPostCreated, circles = [] }) => {
  const [formData, setFormData] = useState({
    title: "",
    content: "",
    circle_id: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      const newPost = await postService.createPost(formData);
      onPostCreated(newPost);
      // Reset form
      setFormData({ title: "", content: "", circle_id: null });
    } catch (err) {
      console.error("Failed to create post:", err);
      setError(err.response?.data?.detail || "Failed to create post");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-post-form">
      <h3>Create New Post</h3>

      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <input
          type="text"
          placeholder="Post title"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
          minLength={1}
          maxLength={100}
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
          minLength={1}
          rows="4"
        />
      </div>

      <div className="form-group">
        <select
          value={formData.circle_id || ""}
          onChange={(e) =>
            setFormData({
              ...formData,
              circle_id: e.target.value ? parseInt(e.target.value) : null,
            })
          }
        >
          <option value="">Public Post (not in a circle)</option>
          {circles.map((circle) => (
            <option key={circle.id} value={circle.id}>
              {circle.name} {circle.badge || ""}
            </option>
          ))}
        </select>
      </div>

      <div className="form-actions">
        <button type="submit" disabled={loading} className="primary-btn">
          {loading ? "Posting..." : "Post"}
        </button>
      </div>
    </form>
  );
};

export default CreatePost;
