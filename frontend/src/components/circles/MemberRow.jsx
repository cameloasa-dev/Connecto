// frontend/src/components/circles/MemberRow.jsx
import { useState } from "react";
import { circleMemberService } from "../../services/circleMember.service";
import "./MemberRow.css";

const MemberRow = ({
  member,
  circleId,
  onRoleChange,
  onRemove,
  currentUserRole,
}) => {
  const [isChanging, setIsChanging] = useState(false);
  const isOwner = member.role === "owner";
  const canManage =
    currentUserRole === "owner" ||
    (currentUserRole === "moderator" && member.role === "member");

  const handleRoleChange = async (newRole) => {
    try {
      setIsChanging(true);
      const updated = await circleMemberService.updateRole(
        circleId,
        member.user_id,
        newRole,
      );
      onRoleChange(updated);
    } catch (error) {
      console.error("Failed to update role:", error);
    } finally {
      setIsChanging(false);
    }
  };

  const handleRemove = async () => {
    if (confirm(`Remove ${member.username} from circle?`)) {
      try {
        await circleMemberService.removeMember(circleId, member.user_id);
        onRemove(member.user_id);
      } catch (error) {
        console.error("Failed to remove member:", error);
      }
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

export default MemberRow;
