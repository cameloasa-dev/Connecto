// frontend/src/components/posts/PostList.jsx
// frontend/src/components/posts/PostList.jsx
import PropTypes from "prop-types";
import PostCard from "./PostCard";
import "./PostList.css";

const PostList = ({ posts, circles }) => {
  if (!posts?.length) {
    return (
      <div className="empty-state">
        <p>No posts yet.</p>
      </div>
    );
  }

  return (
    <div className="posts-grid">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} circles={circles} />
      ))}
    </div>
  );
};

PostList.propTypes = {
  posts: PropTypes.array.isRequired,
  circles: PropTypes.array.isRequired,
};

export default PostList;



