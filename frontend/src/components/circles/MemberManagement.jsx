// frontend/src/components/circles/MemberManagement.jsx
import PropTypes from "prop-types";
import { useState } from "react";
import MemberRow from "./MemberRow";
import AddMemberModal from "./AddMemberModal";
import { useCirclePermissions } from "../../hooks/useCirclePermissions";
import { useAddCircleMember } from "../../hooks/mutations/useCircleMemberMutations";
import { useRemoveCircleMember } from "../../hooks/mutations/useCircleMemberMutations";
import { useUpdateCircleMemberRole } from "../../hooks/mutations/useCircleMemberMutations";
import "./MemberManagement.css";

//eslint-disable-next-line react/prop-types
const MemberManagement = ({ circle, currentUserId }) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);

  const { canManageMembers } = useCirclePermissions(circle);

  const addMember = useAddCircleMember();
  const removeMember = useRemoveCircleMember();
  const updateRole = useUpdateCircleMemberRole();

  const members = circle.members || [];

  const currentUserRole =
    members.find((m) => m.user_id === currentUserId)?.role || null;

  // ADD
  const handleMemberAdded = (userId) => {
    addMember.mutate({
      circleId: circle.id,
      userId,
    });

    setIsAddModalOpen(false);
  };

  // REMOVE
  const handleRemove = (userId) => {
    removeMember.mutate({
      circleId: circle.id,
      userId,
    });
  };

  // ROLE UPDATE
  const handleRoleChange = (userId, role) => {
    updateRole.mutate({
      circleId: circle.id,
      userId,
      role,
    });
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
            onRoleChange={(role) => handleRoleChange(member.user_id, role)}
            onRemove={() => handleRemove(member.user_id)}
            currentUserRole={currentUserRole}
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

MemberManagement.propTypes = {
  circle: PropTypes.shape({
    id: PropTypes.string.isRequired,
    members: PropTypes.arrayOf(
      PropTypes.shape({
        user_id: PropTypes.string.isRequired,
        role: PropTypes.string.isRequired,
      }),
    ),
  }).isRequired,
  currentUserId: PropTypes.string.isRequired,
};

export default MemberManagement;
