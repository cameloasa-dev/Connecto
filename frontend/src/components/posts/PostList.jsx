// frontend/src/components/posts/PostList.jsx

import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import "./PostList.css";

const PostList = ({ posts }) => {
  const navigate = useNavigate();

  if (!posts || posts.length === 0) {
    return (
      <div className="post-list-empty">
        <p>No posts yet. Be the first to write something!</p>
      </div>
    );
  }

  return (
    <div className="post-list-container">
      {posts.map((post) => (
        <div
          key={post.id}
          className="post-list-card"
          onClick={() => navigate(`/post/${post.id}`)}
        >
          <div className="post-list-header">
            <h3 className="post-list-title">{post.title}</h3>
            <span className="post-list-date">
              {new Date(post.created_at).toLocaleDateString()}
            </span>
          </div>

          <p className="post-list-preview">
            {post.content.length > 120
              ? post.content.slice(0, 120) + "..."
              : post.content}
          </p>

          <div className="post-list-footer">
            <span className="post-list-author">@{post.author_username}</span>
            <span className="post-list-likes">❤️ {post.like_count}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

PostList.propTypes = {
  posts: PropTypes.array.isRequired,
};

export default PostList;
