export const validateMemberInvite = ({ email }) => {
  if (!email.includes("@")) {
    return " Invalid Email";
  }
  return null;
};
