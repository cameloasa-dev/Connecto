// frontend/src/components/layout/Navbar.jsx
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/useAuth";
import { useDarkMode } from "../../hooks/useDarkMode";

import { useNavbarSearch } from "../../hooks/navbar/useNavbarSearch";
import { useNavbarDropdown } from "../../hooks/navbar/useNavbarDropdown";
import { usePendingNotifications } from "../../hooks/navbar/usePendingNotifications";

import { NavbarNotificationsDropdown } from "./NavbarNotificationsDropdown";

import "./Navbar.css";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const { isDarkMode, toggleDarkMode } = useDarkMode();
  const { searchQuery, setSearchQuery, handleSearch } = useNavbarSearch();

  const userDropdown = useNavbarDropdown();
  const notifDropdown = useNavbarDropdown();

  const notif = usePendingNotifications();

  const handleLogout = async () => {
    if (window.confirm("Are you sure you want to logout?")) {
      await logout();
      navigate("/login");
    }
  };

  // Public navbar
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

  // Authenticated navbar
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
        {/* Dark mode */}
        <button
          className="navbar-icon"
          onClick={toggleDarkMode}
          title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          <span className="icon">{isDarkMode ? "☀️" : "🌙"}</span>
        </button>

        {/* Notifications */}
        <div className="navbar-icon-wrapper">
          <button
            className="navbar-icon"
            title="Notifications"
            onClick={notifDropdown.toggle}
          >
            <span className="icon">🔔</span>
            {notif.data?.total > 0 && (
              <span className="badge">{notif.data.total}</span>
            )}
          </button>

          {notifDropdown.open && (
            <NavbarNotificationsDropdown
              data={notif.data}
              close={notifDropdown.close}
            />
          )}
        </div>

        {/* User dropdown */}
        <div className="navbar-user" onClick={userDropdown.toggle}>
          <div className="user-avatar">
            {user.username?.charAt(0).toUpperCase()}
          </div>
          <span className="user-name">@{user.username}</span>
          <span className="dropdown-arrow">
            {userDropdown.open ? "▲" : "▼"}
          </span>

          {userDropdown.open && (
            <div className="user-dropdown">
              <button
                className="dropdown-item"
                onClick={() => {
                  userDropdown.close();
                  navigate("/profile");
                }}
              >
                Profile
              </button>

              <div className="dropdown-divider"></div>

              <button
                className="dropdown-item logout"
                onClick={() => {
                  userDropdown.close();
                  handleLogout();
                }}
              >
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
