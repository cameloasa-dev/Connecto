// frontend/src/components/circles/MemberRow.jsx
import propTypes from "prop-types";
import { useState } from "react";
import "./MemberRow.css";

//eslint-disable-next-line react/prop-types
const MemberRow = ({ member, onRoleChange, onRemove, currentUserRole }) => {
  const [isChanging, setIsChanging] = useState(false);

  const isOwner = member.role === "owner";

  const canManage =
    currentUserRole === "owner" ||
    (currentUserRole === "moderator" && member.role === "member");

  const handleRoleChange = async (newRole) => {
    try {
      setIsChanging(true);
      await onRoleChange(newRole);
    } finally {
      setIsChanging(false);
    }
  };

  const handleRemove = async () => {
    const confirmed = window.confirm(`Remove ${member.username} from circle?`);

    if (!confirmed) return;

    try {
      setIsChanging(true);
      await onRemove();
    } finally {
      setIsChanging(false);
    }
  };

  return (
    <div className="member-row">
      <div className="member-info">
        <span className="member-avatar">
          {member.username?.charAt(0).toUpperCase()}
        </span>

        <div className="member-details">
          <div className="member-name">
            {member.username}
            {isOwner && <span className="owner-tag"> (Owner)</span>}
          </div>

          <div className="member-role-badge">
            <span className="badge">{member.badge}</span>
            <span className="role-text">{member.role}</span>
          </div>
        </div>
      </div>

      {!isOwner && canManage && (
        <div className="member-actions">
          <select
            value={member.role}
            onChange={(e) => handleRoleChange(e.target.value)}
            disabled={isChanging}
            className="role-select"
          >
            <option value="member">Member 👤</option>
            <option value="moderator">Moderator 🛡️</option>
          </select>

          <button
            onClick={handleRemove}
            className="remove-btn"
            disabled={isChanging}
            title="Remove member"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
};

MemberRow.propTypes = {
  member: propTypes.shape({
    username: propTypes.string.isRequired,
    role: propTypes.string.isRequired,
    badge: propTypes.string,
  }).isRequired,
  onRoleChange: propTypes.func.isRequired,
  onRemove: propTypes.func.isRequired,
  currentUserRole: propTypes.string.isRequired,
};

export default MemberRow;
