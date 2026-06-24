// frontend/src/pages/LoginPage.jsx
import { useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../contexts/useAuth.js";
import { validateLogin } from "../validation/authValidation.js";
import "./LoginPage.css";

function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const success = location.state?.success || null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // VALIDARE LOCALĂ
    const validationError = validateLogin({ username, password });
    if (validationError) {
      setError(validationError);
      return;
    }

    try {
      const result = await login({ username, password });
      console.log("Login successful:", result);

      navigate("/user-dashboard", { replace: true });
    } catch (err) {
      const message =
        err?.response?.data?.error ||
        err?.message ||
        "Login failed. Please try again.";

      setError(message);
      console.error("Login error:", err);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="login-title">Login to Social Circles</h1>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              name="username"
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              name="password"
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
              disabled={loading}
            />
          </div>

          {success && <div className="success-message">{success}</div>}
          {error && <div className="error-message">{error}</div>}

          <button
            type="submit"
            className="submit-button"
            disabled={loading || !username || !password}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="login-links">
          <p>
            Don&apos;t have an account?{" "}
            <Link to="/register">Register here</Link>
          </p>
          <p>
            <Link to="/forgot-password">Forgot password?</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
