// frontend/src/hooks/circles/useCirclePermissions.js
import { useAuth } from "../../contexts/useAuth";

export const useCirclePermissions = (circle) => {
  const { user } = useAuth();

  const currentMember = circle?.members?.find((m) => m.user_id === user?.id);

  const role = currentMember?.role;

  const isOwner = role === "owner";
  const isModerator = role === "moderator";
  const isMember = !!currentMember;

  return {
    role,
    isOwner,
    isModerator,
    isMember,

    canManageMembers: isOwner || isModerator,
    canChangeRoles: isOwner || isModerator,
    canDeleteCircle: isOwner,
    canPost: isMember,
  };
};
