//src/validation/postValidation.js
export const validatePost = ({ title, content }) => {
  if (!title || title.trim().length < 3) {
    return "Title must have more than 3 characters";
  }
  if (!content || content.trim().length < 5) {
    return "content must have more than 5 characters";
  }
  return null;
};
