import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/useAuth.js";

import PostList from "../components/posts/PostList.jsx";
import PostEditor from "../components/posts/PostEditor.jsx";

import CircleMemberManager from "../components/members/CircleMemberManager.jsx";

import { useCircle } from "../hooks/circles/useCircle";
import { useCirclePosts } from "../hooks/posts/useCirclePosts";

import "./CirclePage.css";

function CirclePage() {
  const { circleId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [showCreatePost, setShowCreatePost] = useState(false);
  const [activeTab, setActiveTab] = useState("posts");

  const { data: circle, isLoading, error } = useCircle(Number(circleId));
  const { data: posts = [] } = useCirclePosts(Number(circleId));

  if (isLoading) {
    return <div className="loading-spinner">Loading circle...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error</h2>
        <p>Failed to load circle</p>

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

  const currentMember = circle.members?.find((m) => m.user_id === user?.id);
  const isOwner = currentMember?.role === "owner";
  const isModerator = currentMember?.role === "moderator";

  return (
    <div className="circle-page">
      {/* HEADER */}
      <div className="circle-header">
        <button
          className="back-btn"
          onClick={() => navigate("/user-dashboard")}
        >
          ← Back
        </button>

        <h1>
          {circle.name} {circle.is_private && "🔒"}
        </h1>

        <div className="circle-badge">
          {isOwner && "👑 Owner"}
          {!isOwner && isModerator && "🛡️ Moderator"}
        </div>

        <p>{circle.description || "No description"}</p>

        <div className="circle-stats">
          <span>Members: {circle.member_count}</span>
          <span>Posts: {posts.length}</span>
        </div>

        <button
          className="primary-btn"
          onClick={() => setShowCreatePost((v) => !v)}
        >
          {showCreatePost ? "Cancel" : "+ Create Post"}
        </button>
      </div>

      {/* CREATE POST */}
      {showCreatePost && (
        <PostEditor
          circles={[circle]}
          onSuccess={() => setShowCreatePost(false)}
          onCancel={() => setShowCreatePost(false)}
        />
      )}

      {/* TABS */}
      <div className="circle-tabs">
        <button
          className={activeTab === "posts" ? "active tab" : "tab"}
          onClick={() => setActiveTab("posts")}
        >
          Posts
        </button>

        <button
          className={activeTab === "members" ? "active tab" : "tab"}
          onClick={() => setActiveTab("members")}
        >
          Members
        </button>
      </div>

      {/* CONTENT */}
      <div className="tab-content">
        {activeTab === "posts" && <PostList posts={posts} circles={[circle]} />}

        {activeTab === "members" && <CircleMemberManager circle={circle} />}
      </div>

      {/* DEBUG */}
      {import.meta.env.DEV && (
        <details className="debug-info">
          <summary>Debug: Raw Data</summary>
          <pre>{JSON.stringify(circle, null, 2)}</pre>
        </details>
      )}
    </div>
  );
}

export default CirclePage;
