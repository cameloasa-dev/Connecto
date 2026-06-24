import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../contexts/useAuth";
import { useDashboardQuery } from "../hooks/dashboard/useDashboardQuery";

import CircleList from "../components/circles/CircleList";
import CircleEditor from "../components/circles/CircleEditor";

import PostEditor from "../components/posts/PostEditor";
import PostList from "../components/posts/PostList";

import "./UserDashboardPage.css";

function UserDashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const [showCreateCircle, setShowCreateCircle] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);

  const {
    data: dashboard,
    isLoading: dashboardLoading,
    error,
    refetch,
  } = useDashboardQuery();

  // Redirect only AFTER auth loading is done
  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login");
    }
  }, [authLoading, user, navigate]);

  // Global loading state
  if (authLoading || dashboardLoading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (!user) return null;

  if (error) {
    return (
      <div className="error-message">
        Failed to load dashboard
        <button className="primary-btn" onClick={() => refetch()}>
          Retry
        </button>
      </div>
    );
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
          onClick={() => setShowCreateCircle(true)}
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

      {/* CREATE CIRCLE MODAL */}
      {showCreateCircle && (
        <div className="circle-editor-overlay">
          <div className="circle-editor-modal">
            <CircleEditor
              circle={null} // 🔥 create mode
              onSuccess={() => {
                setShowCreateCircle(false);
                refetch();
              }}
              onCancel={() => setShowCreateCircle(false)}
            />
          </div>
        </div>
      )}

      {/* CREATE POST */}
      {showCreatePost && (
        <div className="create-post-section">
          <PostEditor
            circles={circles}
            onPostCreated={() => {
              setShowCreatePost(false);
              refetch();
            }}
          />
        </div>
      )}

      {/* ⭐ CIRCLES — CircleList PREMIUM */}
      <section className="circles-section">
        <h2>Your Circles</h2>

        <CircleList
          circles={circles}
          onCreateCircle={() => setShowCreateCircle(true)}
          onOpenCircle={(id) => navigate(`/circles/${id}`)}
        />
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
