export const validateCircle = ({ name, description }) => {
  if (!name || name.trim().length < 3) {
    return "The name of circle must have more than 3 characters";
  }
  if (description && description.length > 300) {
    return "Too long descrription";
  }
  return null;
};
