// frontend/src/pages/UserDashboardPage.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/useAuth.js";
import CreateCircleModal from "../components/circles/CreateCircleModal.jsx";
import CircleCard from "../components/circles/CircleCard.jsx";
import CreatePost from "../components/posts/CreatePost.jsx";
import PostCard from "../components/posts/PostCard.jsx";
import { userDashboardService } from "../services/userDashboard.service.js";
import "./UserDashboardPage.css";

function UserDashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  // State for dashboard data
  const [userDashboardData, setUserDashboardData] = useState({
    user: null,
    circles: [],
    posts: [],
    circlesCount: 0,
    postsCount: 0,
    notificationsCount: 0,
  });

  // State for modals
  const [isCreateCircleModalOpen, setIsCreateCircleModalOpen] = useState(false);
  const [showCreatePost, setShowCreatePost] = useState(false);

  // Loading and error states
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login");
    }
  }, [user, authLoading, navigate]);

  // Load dashboard data
  useEffect(() => {
    const loadUserDashboard = async () => {
      if (!user) return;

      try {
        setLoading(true);
        const data = await userDashboardService.getUserDashboardData();
        setUserDashboardData(data);
      } catch (error) {
        console.error("❌ Failed to load user dashboard:", error);
        setError("Failed to load user dashboard data");
      } finally {
        setLoading(false);
      }
    };

    loadUserDashboard();
  }, [user]);

  // Handler for when a new circle is created
  const handleCircleCreated = (newCircle) => {
    setUserDashboardData((prev) => ({
      ...prev,
      circles: [newCircle, ...prev.circles],
      circlesCount: prev.circlesCount + 1,
    }));
  };

  // Handler for when a new post is created
  const handlePostCreated = (newPost) => {
    setUserDashboardData((prev) => ({
      ...prev,
      posts: [newPost, ...prev.posts],
      postsCount: prev.postsCount + 1,
    }));
  };

  // Handler for create circle button
  const handleCreateCircleClick = () => {
    setIsCreateCircleModalOpen(true);
  };

  if (authLoading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (!user) {
    return null;
  }

  return (
    <>
      <div className="welcome-section">
        <h1>Welcome back, {user.full_name || user.username}! 👋</h1>
        <p>Here's what's happening in your circles.</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading-spinner">Loading dashboard data...</div>
      ) : (
        <>
          {/* Statistics */}
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Your Circles</h3>
              <p className="stat-number">{userDashboardData.circlesCount}</p>
            </div>

            <div className="stat-card">
              <h3>Recent Posts</h3>
              <p className="stat-number">{userDashboardData.postsCount}</p>
            </div>

            <div className="stat-card">
              <h3>Notifications</h3>
              <p className="stat-number">
                {userDashboardData.notificationsCount}
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-buttons">
            <button className="primary-btn" onClick={handleCreateCircleClick}>
              + Create New Circle
            </button>

            <button
              className="secondary-btn"
              onClick={() => setShowCreatePost(!showCreatePost)}
            >
              {showCreatePost ? "Hide" : "Create New Post"}
            </button>
          </div>

          {/* Create Post Form (conditional) */}
          {showCreatePost && (
            <div className="create-post-section">
              <CreatePost
                onPostCreated={handlePostCreated}
                circles={userDashboardData.circles}
              />
            </div>
          )}

          {/* Circles Section with Cards */}
          <section className="circles-section">
            <div className="section-header">
              <h2>Your Circles</h2>
            </div>

            {userDashboardData.circles?.length > 0 ? (
              <div className="circles-grid">
                {userDashboardData.circles.map((circle) => (
                  <CircleCard
                    key={circle.id}
                    circle={circle}
                    onClick={() => navigate(`/circles/${circle.id}`)}
                  />
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <p>You haven't joined any circles yet.</p>
                <button
                  className="primary-btn"
                  onClick={handleCreateCircleClick}
                >
                  Create Your First Circle
                </button>
              </div>
            )}
          </section>

          {/* Recent Posts Feed */}
          <section className="feed-section">
            <h2>Recent Activity</h2>
            {userDashboardData.posts?.length > 0 ? (
              <div className="posts-feed">
                {userDashboardData.posts.map((post) => (
                  <PostCard key={post.id} post={post} showCircle={true} />
                ))}
              </div>
            ) : (
              <p className="empty-message">
                No recent posts in your circles.{" "}
                <button
                  className="link-btn"
                  onClick={() => setShowCreatePost(true)}
                >
                  Create one now!
                </button>
              </p>
            )}
          </section>

          {/* 🔥 Debug info - only in development */}
          {import.meta.env.DEV && (
            <details className="debug-info">
              <summary>Debug: Raw Data</summary>
              <pre>{JSON.stringify(userDashboardData, null, 2)}</pre>
            </details>
          )}
        </>
      )}

      {/* Create Circle Modal */}
      <CreateCircleModal
        isOpen={isCreateCircleModalOpen}
        onClose={() => setIsCreateCircleModalOpen(false)}
        onCircleCreated={handleCircleCreated}
      />
    </>
  );
}

export default UserDashboardPage;
