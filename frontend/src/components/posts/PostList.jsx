// frontend/src/components/posts/PostList.jsx
import PostCard from "./PostCard";

// eslint-disable-next-line react/prop-types
const PostList = ({ posts = [], showCircle = false }) => {
  if (!posts.length) {
    return <p className="empty-message">No posts yet.</p>;
  }

  return (
    <div className="posts-feed">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} showCircle={showCircle} />
      ))}
    </div>
  );
};

export default PostList;
