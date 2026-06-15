import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../contexts/useAuth";
import { useDashboardQuery } from "../hooks/dashboard/useDashboardQuery";

import CreateCircleModal from "../components/circles/CreateCircleModal";
import CircleCard from "../components/circles/CircleCard";

// POSTS (refactor curat)
import CreatePost from "../components/posts/CreatePost";
import PostList from "../components/posts/PostList";

import "./UserDashboardPage.css";

function UserDashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [isCreateCircleModalOpen, setIsCreateCircleModalOpen] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login");
    }
  }, [authLoading, user, navigate]);

  const { data: dashboard, isLoading, error } = useDashboardQuery();

  if (authLoading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (!user) {
    return null;
  }

  if (isLoading) {
    return <div className="loading-spinner">Loading dashboard data...</div>;
  }

  if (error) {
    return <div className="error-message">Failed to load dashboard data</div>;
  }

  const circles = dashboard?.circles ?? [];
  const posts = dashboard?.feed ?? []; // IMPORTANT: feed contains recent posts from all circles the user is part of

  return (
    <>
      <div className="welcome-section">
        <h1>Welcome back, {user.full_name || user.username}! 👋</h1>
        <p>Here&apos;s what&apos;s happening in your circles.</p>
      </div>

      {/* ACTIONS */}
      <div className="action-buttons">
        <button
          className="primary-btn"
          onClick={() => setIsCreateCircleModalOpen(true)}
        >
          + Create New Circle
        </button>

        <button
          className="secondary-btn"
          onClick={() => setShowCreatePost((prev) => !prev)}
        >
          {showCreatePost ? "Hide" : "Create New Post"}
        </button>
      </div>

      {/* CREATE POST */}
      {showCreatePost && (
        <div className="create-post-section">
          <CreatePost circles={circles} />
        </div>
      )}

      {/* CIRCLES (nemodificat) */}
      <section className="circles-section">
        <div className="section-header">
          <h2>Your Circles</h2>
        </div>

        {circles.length > 0 ? (
          <div className="circles-grid">
            {circles.map((circle) => (
              <CircleCard
                key={circle.id}
                circle={circle}
                onClick={() => navigate(`/circles/${circle.id}`)}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>You haven&apos;t joined any circles yet.</p>

            <button
              className="primary-btn"
              onClick={() => setIsCreateCircleModalOpen(true)}
            >
              Create Your First Circle
            </button>
          </div>
        )}
      </section>

      {/* POSTS FEED (REFACUTAT) */}
      <section className="feed-section">
        <h2>Recent Activity</h2>

        {posts.length > 0 ? (
          <PostList posts={posts} />
        ) : (
          <p className="empty-message">
            No recent posts in your circles.
            <button
              className="link-btn"
              onClick={() => setShowCreatePost(true)}
            >
              Create one now!
            </button>
          </p>
        )}
      </section>

      {/* DEBUG */}
      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug: Raw Data</summary>
          <pre>{JSON.stringify(dashboard, null, 2)}</pre>
        </details>
      )}

      <CreateCircleModal
        isOpen={isCreateCircleModalOpen}
        onClose={() => setIsCreateCircleModalOpen(false)}
      />
    </>
  );
}

export default UserDashboardPage;
