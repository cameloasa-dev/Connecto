// frontend/src/pages/CirclePage.jsx
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/useAuth.js";
import CreatePost from "../components/posts/CreatePost.jsx";
import PostCard from "../components/posts/PostCard.jsx";
import MemberManagement from "../components/circles/MemberManagement";
import CircleSettings from "../components/circles/CircleSettings";
import { circleService } from "../services/circle.service";
import { postService } from "../services/post.service";
import "./CirclePage.css";

function CirclePage() {
  const { circleId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [circle, setCircle] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreatePost, setShowCreatePost] = useState(false);
  const [activeTab, setActiveTab] = useState("posts");

  // Load circle data
  useEffect(() => {
    const fetchCircleData = async () => {
      try {
        setLoading(true);
        setError("");

        const [circleData, postsData] = await Promise.all([
          circleService.getCircle(circleId),
          postService.getCirclePosts(circleId),
        ]);

        setCircle(circleData);
        setPosts(postsData || []);
      } catch (err) {
        console.error("Failed to load circle:", err);
        if (err.response?.status === 403) {
          setError("You are not a member of this circle");
        } else if (err.response?.status === 404) {
          setError("Circle not found");
        } else {
          setError("Failed to load circle data");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCircleData();
  }, [circleId]);

  const handlePostCreated = (newPost) => {
    setPosts([newPost, ...posts]);
    setShowCreatePost(false);
  };

  const handleMemberUpdated = (updatedData) => {
    if (updatedData.type === "remove") {
      setCircle((prev) => ({
        ...prev,
        members: prev.members.filter((m) => m.user_id !== updatedData.userId),
        member_count: prev.member_count - 1,
      }));
    } else if (updatedData.member) {
      setCircle((prev) => {
        const existingIndex = prev.members.findIndex(
          (m) => m.user_id === updatedData.member.user_id,
        );

        if (existingIndex >= 0) {
          const newMembers = [...prev.members];
          newMembers[existingIndex] = updatedData.member;
          return { ...prev, members: newMembers };
        } else {
          return {
            ...prev,
            members: [...prev.members, updatedData.member],
            member_count: prev.member_count + 1,
          };
        }
      });
    }
  };

  const handleCircleUpdated = (updatedCircle) => {
    setCircle(updatedCircle);
  };

  const currentUserRole = circle?.members?.find(
    (m) => m.user_id === user?.id,
  )?.role;
  const isOwner = currentUserRole === "owner";
  const isModerator = currentUserRole === "moderator";
  const canChangeSettings = isOwner;

  if (loading) {
    return <div className="loading-spinner">Loading circle...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>{error}</p>
        <button
          className="primary-btn"
          onClick={() => navigate("/user-dashboard")}
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  if (!circle) return null;

  return (
    <div className="circle-page">
      {/* Circle Header */}
      <div className="circle-header">
        <div className="circle-header-content">
          <button
            className="back-btn"
            onClick={() => navigate("/user-dashboard")}
          >
            ← Back to Dashboard
          </button>

          <div className="circle-title-section">
            <h1>{circle.name}</h1>
            <div className="circle-badge">
              {isOwner && "👑 Owner"}
              {isModerator && "🛡️ Moderator"}
            </div>
          </div>

          <p className="circle-description">
            {circle.description || "No description"}
          </p>

          <div className="circle-stats">
            <div className="stat">
              <span className="stat-value">{circle.member_count}</span>
              <span className="stat-label">Members</span>
            </div>
            <div className="stat">
              <span className="stat-value">{posts.length}</span>
              <span className="stat-label">Posts</span>
            </div>
            <div className="stat">
              <span className="stat-value">📅</span>
              <span className="stat-label">
                Created {new Date(circle.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>

          <div className="circle-actions">
            <button
              className="primary-btn"
              onClick={() => setShowCreatePost(!showCreatePost)}
            >
              {showCreatePost ? "Cancel" : "+ Create Post"}
            </button>
          </div>

          {showCreatePost && (
            <div className="create-post-section">
              <CreatePost
                onPostCreated={handlePostCreated}
                circles={[circle]}
                selectedCircleId={circle.id}
              />
            </div>
          )}
        </div>
      </div>

      <div className="circle-tabs">
        <button
          className={`tab ${activeTab === "posts" ? "active" : ""}`}
          onClick={() => setActiveTab("posts")}
        >
          Posts ({posts.length})
        </button>
        <button
          className={`tab ${activeTab === "members" ? "active" : ""}`}
          onClick={() => setActiveTab("members")}
        >
          Members ({circle.member_count})
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "posts" && (
          <div className="posts-section">
            {posts.length > 0 ? (
              posts.map((post) => <PostCard key={post.id} post={post} />)
            ) : (
              <div className="empty-state">
                <p>No posts in this circle yet.</p>
                <button
                  className="primary-btn"
                  onClick={() => setShowCreatePost(true)}
                >
                  Create First Post
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === "members" && (
          <div className="members-section">
            <MemberManagement
              circle={circle}
              members={circle.members || []}
              onMemberUpdated={handleMemberUpdated}
              currentUserId={user?.id}
            />

            {canChangeSettings && (
              <CircleSettings
                circle={circle}
                onCircleUpdated={handleCircleUpdated}
              />
            )}
          </div>
        )}
      </div>

      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug: Circle Data</summary>
          <pre>{JSON.stringify(circle, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}

export default CirclePage;
