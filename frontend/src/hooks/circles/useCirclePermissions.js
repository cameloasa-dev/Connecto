// frontend/src/hooks/useCirclePermissions.js
import { useAuth } from "../../contexts/useAuth";

export const useCirclePermissions = (circle) => {
  const { user } = useAuth();

  // If no circle or user → all permissions false
  if (!circle || !user) {
    return {
      isOwner: false,
      isModerator: false,
      isMember: false,
      canModerate: false,
      canManageMembers: false,
      canChangeRoles: false,
      canDeleteCircle: false,
      canChangeSettings: false,
    };
  }

  // Find the current member in circle.members
  const currentMember = circle.members?.find((m) => m.user_id === user.id);

  const role = currentMember?.role || null;

  const isOwner = role === "owner";
  const isModerator = role === "moderator";
  const isMember = !!currentMember;

  return {
    isOwner,
    isModerator,
    isMember,
    canModerate: isOwner || isModerator,
    canManageMembers: isOwner || isModerator,
    canChangeRoles: isOwner,
    canDeleteCircle: isOwner,
    canChangeSettings: isOwner,
  };
};
