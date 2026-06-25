// frontend/src/pages/PostPage.jsx

import { useParams, useNavigate } from "react-router-dom";

import { usePost } from "../hooks/posts/useCirclePosts";
import { useCirclePermissions } from "../hooks/circles/useCirclePermissions";
import { useToggleLike } from "../hooks/mutations/useCommentMutations";

import PostCard from "../components/posts/PostCard";

import { CommentList } from "../components/comments/CommentList";
import { CommentForm } from "../components/comments/CommentForm";

import "./PostPage.css";

function PostPage() {
  const { postId } = useParams();
  const navigate = useNavigate();

  const { data: post, isLoading, error } = usePost(Number(postId));

  const { isModerator } = useCirclePermissions(post?.circle_id);

  const toggleLike = useToggleLike();

  if (isLoading) return <div className="loading-spinner">Loading post...</div>;
  if (error) return <div className="error-container">Failed to load post</div>;
  if (!post) return null;

  const handleLike = () => {
    toggleLike.mutate(post.id);
  };

  return (
    <div className="post-page">
      {/* BACK BUTTON */}
      <button
        className="back-btn"
        onClick={() => navigate(`/circle/${post.circle_id}`)}
      >
        ← Back to Circle
      </button>

      {/* POST HEADER */}
      <div className="post-header">
        <h1 className="post-title">{post.title}</h1>

        <div className="post-meta">
          <span className="post-author">@{post.author_username}</span>
          <span className="post-date">
            {new Date(post.created_at).toLocaleString()}
          </span>
        </div>

        <div className="post-circle-link">
          In circle:{" "}
          <span
            className="circle-link"
            onClick={() => navigate(`/circle/${post.circle_id}`)}
          >
            {post.circle_name}
          </span>
        </div>

        {/* LIKE BUTTON */}
        <button className="like-btn" onClick={handleLike}>
          {post.is_liked_by_user ? "❤️ Liked" : "🤍 Like"} ({post.like_count})
        </button>
      </div>

      {/* POST CONTENT */}
      <PostCard
        post={post}
        circles={[{ id: post.circle_id, name: post.circle_name }]}
      />

      {/* COMMENTS SECTION */}
      <div className="comments-section">
        <h2>Comments</h2>

        {/* APPROVED COMMENTS */}
        <CommentList
          comments={post.comments?.approved || []}
          postId={post.id}
          circleId={post.circle_id}
        />

        {/* ADD COMMENT */}
        <CommentForm postId={post.id} />

        {/* PENDING COMMENTS (moderators only) */}
        {isModerator && post.comments?.pending?.length > 0 && (
          <div className="pending-comments">
            <h3>Pending Approval</h3>

            <CommentList
              comments={post.comments.pending}
              postId={post.id}
              circleId={post.circle_id}
            />
          </div>
        )}
      </div>

      {/* DEBUG */}
      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug: Raw Post</summary>
          <pre>{JSON.stringify(post, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}

export default PostPage;
