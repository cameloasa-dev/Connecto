// frontend/src/components/circles/MemberManagement.jsx
import { useState } from "react";
import MemberRow from "./MemberRow";
import AddMemberModal from "./AddMemberModal";
import { useCirclePermissions } from "../../hooks/useCirclePermissions";
import "./MemberManagement.css";

const MemberManagement = ({
  circle,
  members,
  onMemberUpdated,
  currentUserId,
}) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const { canManageMembers } = useCirclePermissions(circle);

  // Users roles are determined by the members list, so we find the current user's role from there
  const getCurrentUserRole = () => {
    const currentUser = members.find((m) => m.user_id === currentUserId);
    return currentUser?.role || null;
  };

  const currentUserRole = getCurrentUserRole();

  const handleRoleChange = (updatedMember) => {
    onMemberUpdated(updatedMember);
  };

  const handleRemove = (userId) => {
    onMemberUpdated({ type: "remove", userId });
  };

  const handleMemberAdded = (newMember) => {
    onMemberUpdated(newMember);
    setIsAddModalOpen(false);
  };

  return (
    <div className="member-management">
      <div className="member-header">
        <h3>Members ({members.length})</h3>
        {canManageMembers && (
          <button
            className="add-member-btn"
            onClick={() => setIsAddModalOpen(true)}
          >
            + Add Member
          </button>
        )}
      </div>

      <div className="member-list">
        {members.map((member) => (
          <MemberRow
            key={member.user_id}
            member={member}
            circleId={circle.id}
            onRoleChange={handleRoleChange}
            onRemove={handleRemove}
            currentUserRole={currentUserRole} // send current user's role to determine permissions in MemberRow
          />
        ))}
      </div>

      <AddMemberModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        circleId={circle.id}
        onMemberAdded={handleMemberAdded}
      />
    </div>
  );
};

export default MemberManagement;
