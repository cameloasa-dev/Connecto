// frontend/src/components/layout/Navbar.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/useAuth";
import { useDarkMode } from "../../hooks/useDarkMode";
import "./Navbar.css";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const { isDarkMode, toggleDarkMode } = useDarkMode();
  const [searchQuery, setSearchQuery] = useState("");

  const handleLogout = async () => {
    if (window.confirm("Are you sure you want to logout?")) {
      try {
        await logout();
        navigate("/login");
      } catch (error) {
        console.error("Logout failed:", error);
        alert("Logout failed. Please try again.");
      }
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery("");
    }
  };

  // If no user, show minimal navbar for public pages
  if (!user) {
    return (
      <header className="navbar">
        <div className="navbar-left">
          <div className="navbar-logo" onClick={() => navigate("/")}>
            Social Circles
          </div>
        </div>
        <div className="navbar-right">
          <button className="nav-btn" onClick={() => navigate("/login")}>
            Login
          </button>
          <button
            className="nav-btn primary"
            onClick={() => navigate("/register")}
          >
            Register
          </button>
        </div>
      </header>
    );
  }

  // Navbar for authenticated users
  return (
    <header className="navbar">
      <div className="navbar-left">
        <div
          className="navbar-logo"
          onClick={() => navigate("/user-dashboard")}
        >
          Social Circles
        </div>
        <form onSubmit={handleSearch} className="navbar-search">
          <input
            type="text"
            placeholder="Search circles, posts, people..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn">
            🔍
          </button>
        </form>
      </div>

      <div className="navbar-right">
        {/* Dark Mode Toggle Button */}
        <button
          className="navbar-icon"
          onClick={toggleDarkMode}
          title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          <span className="icon">{isDarkMode ? "☀️" : "🌙"}</span>
        </button>

        <button className="navbar-icon" title="Notifications">
          <span className="icon">🔔</span>
          <span className="badge">3</span>
        </button>

        <button className="navbar-icon" title="Messages">
          <span className="icon">✉️</span>
        </button>

        <div
          className="navbar-user"
          onClick={() => setShowDropdown(!showDropdown)}
        >
          <div className="user-avatar">
            {user.username?.charAt(0).toUpperCase() || "U"}
          </div>
          <span className="user-name">@{user.username}</span>
          <span className="dropdown-arrow">{showDropdown ? "▲" : "▼"}</span>

          {showDropdown && (
            <div className="user-dropdown">
              <button
                className="dropdown-item"
                onClick={() => {
                  setShowDropdown(false);
                  navigate("/profile");
                }}
              >
                Profile
              </button>
              <button
                className="dropdown-item"
                onClick={() => {
                  setShowDropdown(false);
                  navigate("/settings");
                }}
              >
                Settings
              </button>
              <div className="dropdown-divider"></div>
              <button className="dropdown-item logout" onClick={handleLogout}>
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

export default Navbar;
