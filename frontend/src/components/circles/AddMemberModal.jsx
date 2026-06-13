// frontend/src/components/circles/AddMemberModal.jsx
import { useState } from "react";
import PropTypes from "prop-types";
import { useSearchUsers } from "../../hooks/search/useSearchUsersMutation";
import { useAddCircleMember } from "../../hooks/mutations/useCircleMemberMutations";
import "./AddMemberModal.css";

const AddMemberModal = ({ isOpen, onClose, circleId, onMemberAdded }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  const { mutate: searchUsers, isPending: isSearching } = useSearchUsers();
  const { mutate: addMember, isPending: isAdding } = useAddCircleMember();

  if (!isOpen) return null;

  const handleSearch = () => {
    if (!searchQuery.trim()) return;

    searchUsers(
      { query: searchQuery, circleId },
      {
        onSuccess: (results) => {
          setSearchResults(results);
        },
        onError: () => {
          setSearchResults([]);
        },
      },
    );
  };

  const handleAddMember = (userId) => {
    addMember(
      { circleId, userId },
      {
        onSuccess: (newMember) => {
          onMemberAdded(newMember);

          // remove user from search results
          setSearchResults((prev) =>
            prev.filter((user) => user.id !== userId),
          );
        },
      },
    );
  };

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
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="search-input"
              autoFocus
            />

            <button
              onClick={handleSearch}
              disabled={isSearching || !searchQuery.trim()}
              className="search-btn"
            >
              {isSearching ? "Searching..." : "Search"}
            </button>
          </div>

          <div className="search-results">
            {searchResults.length > 0 ? (
              searchResults.map((user) => (
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
                    disabled={isAdding}
                    className="add-btn"
                  >
                    {isAdding ? "Adding..." : "Add"}
                  </button>
                </div>
              ))
            ) : (
              searchQuery &&
              !isSearching && (
                <p className="no-results">
                  No users found matching &quot;{searchQuery}&quot;
                </p>
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

AddMemberModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  circleId: PropTypes.string.isRequired,
  onMemberAdded: PropTypes.func.isRequired,
};

export default AddMemberModal;