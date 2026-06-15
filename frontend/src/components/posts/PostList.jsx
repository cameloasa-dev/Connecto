// frontend/src/components/posts/PostList.jsx
import PostCard from "./PostCard";
import propTypes from "prop-types";

const PostList = ({ posts = [] }) => {
  if (!posts.length) {
    return <p className="empty-message">No posts yet.</p>;
  }

  return (
    <div className="posts-feed">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
};

PostList.propTypes = {
  posts: propTypes.arrayOf(
    propTypes.shape({
      id: propTypes.number.isRequired,
      title: propTypes.string.isRequired,
      content: propTypes.string.isRequired,
    }),
  ).isRequired,
};

export default PostList;
