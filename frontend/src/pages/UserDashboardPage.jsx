import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../contexts/useAuth";
import { useDashboardQuery } from "../hooks/dashboard/useDashboardQuery";

import CircleCard from "../components/circles/CircleCard";
import CreatePost from "../components/posts/CreatePost";
import PostList from "../components/posts/PostList";

import "./UserDashboardPage.css";

function UserDashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [showCreatePost, setShowCreatePost] = useState(false);

  const { data: dashboard, isLoading, error } = useDashboardQuery();

  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login");
    }
  }, [authLoading, user, navigate]);

  if (authLoading || isLoading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (!user) return null;

  if (error) {
    return <div className="error-message">Failed to load dashboard</div>;
  }

  const circles = dashboard?.circles ?? [];
  const posts = dashboard?.feed ?? [];

  return (
    <div className="dashboard">
      {/* HEADER */}
      <div className="welcome-section">
        <h1>Welcome back, {user.full_name || user.username} 👋</h1>
        <p>Your circles and activity overview</p>
      </div>

      {/* ACTIONS */}
      <div className="action-buttons">
        <button
          className="primary-btn"
          onClick={() => navigate("/circles/create")}
        >
          + Create Circle
        </button>

        <button
          className="secondary-btn"
          onClick={() => setShowCreatePost((v) => !v)}
        >
          {showCreatePost ? "Hide Post Creator" : "Create Post"}
        </button>
      </div>

      {/* CREATE POST */}
      {showCreatePost && (
        <div className="create-post-section">
          <CreatePost circles={circles} />
        </div>
      )}

      {/* CIRCLES */}
      <section className="circles-section">
        <h2>Your Circles</h2>

        {circles.length ? (
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
            <p>You are not part of any circles yet.</p>

            <button
              className="primary-btn"
              onClick={() => navigate("/circles/create")}
            >
              Create your first circle
            </button>
          </div>
        )}
      </section>

      {/* FEED */}
      <section className="feed-section">
        <h2>Recent Activity</h2>

        {posts.length ? (
          <PostList posts={posts} />
        ) : (
          <div className="empty-state">
            <p>No recent activity.</p>
          </div>
        )}
      </section>

      {/* DEBUG */}
      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug: Raw Data</summary>
          <pre>{JSON.stringify(dashboard, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}

export default UserDashboardPage;
