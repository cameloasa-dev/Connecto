// frontend/src/components/circles/AddMemberModal.jsx
import { useState } from "react";
import { circleMemberService } from "../../services/circleMember.service";
import "./AddMemberModal.css";

// eslint-disable-next-line react/prop-types
const AddMemberModal = ({ isOpen, onClose, circleId, onMemberAdded }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);
    try {
      console.log("🔍 Searching for:", searchQuery, "in circle:", circleId);
      const results = await circleMemberService.searchUsers(
        searchQuery,
        circleId,
      );
      console.log("✅ Search results:", results);
      setSearchResults(results);
    } catch (err) {
      console.error("❌ Search failed - Full error:", err);
      console.error("❌ Response data:", err.response?.data);
      console.error("❌ Response status:", err.response?.status);
      setError("Search failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleAddMember = async (userId) => {
    try {
      const newMember = await circleMemberService.addMember(circleId, userId);
      onMemberAdded(newMember);
      // Remove from search results
      setSearchResults((prev) => prev.filter((user) => user.id !== userId));
    } catch (err) {
      setError("Failed to add member. Please try again.");
      console.error("Failed to add member:", err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h2>Add Member to Circle</h2>
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="modal-body">
          <div className="search-section">
            <input
              type="text"
              placeholder="Search by username..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSearch()}
              className="search-input"
              autoFocus
            />
            <button
              onClick={handleSearch}
              disabled={loading || !searchQuery.trim()}
              className="search-btn"
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="search-results">
            {searchResults.length > 0
              ? searchResults.map((user) => (
                  <div key={user.id} className="user-result">
                    <div className="user-info">
                      <span className="user-avatar">
                        {user.username.charAt(0).toUpperCase()}
                      </span>
                      <div>
                        <div className="user-name">{user.username}</div>
                        <div className="user-email">{user.email}</div>
                      </div>
                    </div>
                    <button
                      onClick={() => handleAddMember(user.id)}
                      className="add-btn"
                    >
                      Add
                    </button>
                  </div>
                ))
              : searchQuery &&
                !loading && (
                  <p className="no-results">
                    No users found matching "{searchQuery}"
                  </p>
                )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddMemberModal;
