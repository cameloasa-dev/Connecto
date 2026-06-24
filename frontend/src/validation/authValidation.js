export const validateLogin = ({ username, password }) => {
  if (!username || username.length < 3) {
    return "Username must be at least 3 characters";
  }

  if (!password || password.length < 1) {
    return "Password is required";
  }

  return null;
};

import { validatePassword } from "./passwordValidation";

export const validateRegister = ({
  username,
  email,
  password,
  confirmPassword,
}) => {
  if (!username || username.length < 3 || username.length > 50) {
    return "Username must be between 3 and 50 characters";
  }

  if (!email || !email.includes("@")) {
    return "Invalid email address";
  }

  const passwordError = validatePassword(password);
  if (passwordError) return passwordError;

  if (password !== confirmPassword) {
    return "Passwords do not match";
  }

  return null;
};
