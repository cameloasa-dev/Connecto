import PropTypes from "prop-types";
import PostActions from "./PostActions";
import "./PostCard.css";

const PostCard = ({ post, showCircle = false }) => {
  return (
    <div className="post-card">
      <div className="post-header">
        <div className="post-author-avatar">
          {post.author_name?.charAt(0).toUpperCase() || "U"}
        </div>

        <div className="post-author-info">
          <div className="post-author">{post.author_name}</div>
          <div className="post-date">
            {new Date(post.created_at).toLocaleDateString()}
          </div>
        </div>
      </div>

      <div className="post-content">
        <h4>{post.title}</h4>
        <p>{post.content}</p>

        {showCircle && post.circle_name && (
          <div className="post-circle">in {post.circle_name}</div>
        )}
      </div>

      <PostActions />
    </div>
  );
};

PostCard.propTypes = {
  showCircle: PropTypes.bool,
  post: PropTypes.shape({
    author_name: PropTypes.string,
    created_at: PropTypes.string,
    title: PropTypes.string,
    content: PropTypes.string,
    circle_name: PropTypes.string,
  }).isRequired,
};

export default PostCard;
