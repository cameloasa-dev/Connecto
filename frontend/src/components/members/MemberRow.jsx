//frontend/src/components/members/MemberRow
import { useState } from "react";
import PropTypes from "prop-types";

import "./MemberRow.css";

const MemberRow = ({ member, canManageMembers, onRoleChange, onRemove }) => {
  const [isChanging, setIsChanging] = useState(false);

  const isOwner = member.role === "owner";
  const canManage = canManageMembers && !isOwner;

  const handleRoleChange = async (e) => {
    const newRole = e.target.value;

    try {
      setIsChanging(true);
      await onRoleChange(newRole);
    } finally {
      setIsChanging(false);
    }
  };

  const handleRemove = async () => {
    const ok = window.confirm(`Remove ${member.username} from circle?`);

    if (!ok) return;

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
        <div className="member-avatar">
          {member.username?.charAt(0).toUpperCase()}
        </div>

        <div className="member-details">
          <div className="member-name">
            {member.username}
            {isOwner && <span className="owner-tag"> (Owner)</span>}
          </div>

          <div className="member-role">
            <span className="role-text">{member.role}</span>
          </div>
        </div>
      </div>

      {canManage && (
        <div className="member-actions">
          <select
            value={member.role}
            onChange={handleRoleChange}
            disabled={isChanging}
            className="role-select"
          >
            <option value="member">Member</option>
            <option value="moderator">Moderator</option>
          </select>

          <button
            onClick={handleRemove}
            disabled={isChanging}
            className="remove-btn"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  );
};

MemberRow.propTypes = {
  member: PropTypes.shape({
    username: PropTypes.string.isRequired,
    role: PropTypes.string.isRequired,
  }).isRequired,

  canManageMembers: PropTypes.bool.isRequired,
  onRoleChange: PropTypes.func.isRequired,
  onRemove: PropTypes.func.isRequired,
};

export default MemberRow;
