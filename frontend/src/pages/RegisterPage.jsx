// frontend/src/pages/RegisterPage.jsx
import { useState } from "react";
import { useAuth } from "../contexts/useAuth.js";
import { useNavigate, Link } from "react-router-dom";
import { validateRegister } from "../validation/authValidation.js";
import "./RegisterPage.css";

function RegisterPage() {
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const { register, loading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validation error
    const validationError = validateRegister({
      username,
      email,
      password,
      confirmPassword,
      fullName,
    });

    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      const userData = {
        username,
        password,
        full_name: fullName,
        email,
      };

      const result = await register(userData);

      const message = `Account created for ${
        result.username || username
      }! You can now login.`;

      navigate("/login", { state: { success: message } });
    } catch (err) {
      const message =
        err?.response?.data?.error ||
        err?.message ||
        "Registration failed. Please try again.";

      setError(message);
      console.error("Registration error:", err);
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h1 className="register-title">Create Account</h1>

        <form onSubmit={handleSubmit} className="register-form">
          {/* Username */}
          <div className="form-group">
            <label htmlFor="username">Username *</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Choose a username"
              required
              disabled={loading}
              minLength="3"
              maxLength="50"
            />
            <small className="form-hint">
              3–50 characters, letters and numbers only
            </small>
          </div>

          {/* Full Name */}
          <div className="form-group">
            <label htmlFor="fullName">Full Name (Optional)</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Your full name"
              disabled={loading}
              minLength="2"
              maxLength="100"
            />
          </div>

          {/* Email */}
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Your email address"
              required
              disabled={loading}
            />
          </div>

          {/* Password */}
          <div className="form-group">
            <label htmlFor="password">Password *</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Create a password"
              required
              disabled={loading}
              minLength="8"
            />
            <small className="form-hint">
              Must include upper & lower case letters, numbers and special
              characters
            </small>
          </div>

          {/* Confirm Password */}
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password *</label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm your password"
              required
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            className="submit-button"
            disabled={
              loading || !username || !email || !password || !confirmPassword
            }
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <div className="register-links">
          <p>
            Already have an account? <Link to="/login">Login here</Link>
          </p>
          <p className="terms-note">
            By registering, you agree to our{" "}
            <Link to="/terms">Terms of Service</Link> and{" "}
            <Link to="/privacy">Privacy Policy</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
