// frontend/src/components/members/CircleMemberManager.jsx
import { useState } from "react";
import PropTypes from "prop-types";

import MemberRow from "./MemberRow";
import { useCirclePermissions } from "../../hooks/circles/useCirclePermissions";

// SEARCH
import { useSearchUsersQuery } from "../../hooks/search/useSearchUsersQuery";

// MUTATIONS
import {
  useAddCircleMember,
  useRemoveCircleMember,
  useUpdateCircleMemberRole,
} from "../../hooks/mutations/useCircleMemberMutations";

import "./CircleMemberManager.css";

const CircleMemberManager = ({ circle }) => {
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [search, setSearch] = useState("");

  const { canManageMembers } = useCirclePermissions(circle);

  const members = circle.members || [];

  // SEARCH USERS
  const { data: users = [], isLoading: isSearching } = useSearchUsersQuery(
    search,
    circle.id,
  );

  // MUTATIONS
  const addMember = useAddCircleMember();
  const removeMember = useRemoveCircleMember();
  const updateRole = useUpdateCircleMemberRole();

  // ======================
  // HANDLERS
  // ======================

  const handleAddMember = (userId) => {
    addMember.mutate({
      circleId: circle.id,
      userId,
    });

    setSearch("");
  };

  const handleRemove = (userId) => {
    removeMember.mutate({
      circleId: circle.id,
      userId,
    });
  };

  const handleRoleChange = (userId, role) => {
    updateRole.mutate({
      circleId: circle.id,
      userId,
      role,
    });
  };

  return (
    <div className="circle-member-manager">
      {/* HEADER */}
      <div className="member-header">
        <h3>Members ({members.length})</h3>

        {canManageMembers && (
          <button
            className="add-member-btn"
            onClick={() => setIsAddOpen((v) => !v)}
          >
            {isAddOpen ? "Close" : "+ Add Member"}
          </button>
        )}
      </div>

      {/* ADD MEMBER PANEL */}
      {isAddOpen && (
        <div className="add-member-panel">
          <input
            type="text"
            placeholder="Search users..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          {isSearching && <p className="loading">Searching...</p>}

          <div className="search-results">
            {users.map((user) => (
              <div key={user.id} className="search-user">
                <span>{user.username}</span>

                <button
                  onClick={() => handleAddMember(user.id)}
                  className="add-btn"
                >
                  Add
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* MEMBERS LIST */}
      <div className="member-list">
        {members.map((member) => (
          <MemberRow
            key={member.user_id}
            member={member}
            circle={circle}
            canManage={canManageMembers}
            onRoleChange={(role) => handleRoleChange(member.user_id, role)}
            onRemove={() => handleRemove(member.user_id)}
          />
        ))}
      </div>
    </div>
  );
};

CircleMemberManager.propTypes = {
  circle: PropTypes.object.isRequired,
};

export default CircleMemberManager;
