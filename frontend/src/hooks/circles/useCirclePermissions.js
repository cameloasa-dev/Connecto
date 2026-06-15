// frontend/src/hooks/circles/useCirclePermissions.js
import { useAuth } from "../../contexts/useAuth";

export const useCirclePermissions = (circle) => {
  const { user } = useAuth();

  const currentMember = circle?.members?.find((m) => m.user_id === user?.id);

  const role = currentMember?.role || null;

  const isOwner = role === "owner";
  const isModerator = role === "moderator";
  const isMember = !!currentMember;

  return {
    // identity
    role,
    isOwner,
    isModerator,
    isMember,

    // permissions
    canModerate: isOwner || isModerator,
    canManageMembers: isOwner || isModerator,
    canChangeRoles: isOwner,
    canDeleteCircle: isOwner,
    canPost: isMember,
  };
};
