import { useParams, useNavigate } from "react-router-dom";
import { useUserProfileQuery } from "../hooks/profile/useUserProfileQuery";
import PostList from "../components/posts/PostList";
import CircleList from "../components/circles/CircleList";
import "./ProfilePage.css";

function ProfilePage() {
  const { userId } = useParams();
  const navigate = useNavigate();

  const { data, isLoading, error } = useUserProfileQuery(Number(userId));

  if (isLoading)
    return <div className="loading-spinner">Loading profile...</div>;

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>Failed to load profile</p>

        <button className="primary-btn" onClick={() => navigate(-1)}>
          Go Back
        </button>
      </div>
    );
  }

  if (!data) return null;

  const { user, posts, circles } = data;

  return (
    <main className="profile-page">
      {/* HEADER */}
      <div className="profile-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>

        <div className="profile-avatar">
          {user.username.charAt(0).toUpperCase()}
        </div>

        <h1>{user.username}</h1>
        <p className="profile-email">{user.email}</p>
      </div>

      {/* STATS */}
      <div className="profile-stats">
        <div className="stat-box">
          <strong>{posts.length}</strong>
          <span>Posts</span>
        </div>

        <div className="stat-box">
          <strong>{circles.length}</strong>
          <span>Circles</span>
        </div>
      </div>

      {/* POSTS */}
      <section className="profile-section">
        <h2>User Posts</h2>
        <PostList posts={posts} />
      </section>

      {/* CIRCLES */}
      <section className="profile-section">
        <h2>Member of Circles</h2>
        <CircleList circles={circles} />
      </section>

      {/* DEBUG */}
      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug: Raw Profile Data</summary>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </details>
      )}
    </main>
  );
}

export default ProfilePage;
