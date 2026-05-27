// frontend/src/components/layout/UserSidebar.jsx
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./UserSidebar.css";

function UserSidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isOpen, setIsOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  // Detect screen size changes
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
      if (window.innerWidth > 768) {
        setIsOpen(true); // Always open on desktop
      } else {
        setIsOpen(false); // Closed by default on mobile
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize(); // Initial check

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const menuItems = [
    { icon: "🏠", label: "Dashboard", path: "/user-dashboard" },
    { icon: "🔍", label: "Explore", path: "/explore" },
    { icon: "⚙️", label: "Settings", path: "/settings" },
    { icon: "❓", label: "Help", path: "/help" },
  ];

  const isActive = (path) => location.pathname === path;

  const handleItemClick = (path) => {
    navigate(path);
    if (isMobile) {
      setIsOpen(false); // Close sidebar after navigation on mobile
    }
  };

  return (
    <>
      {/* Hamburger button - only visible on mobile */}
      {isMobile && (
        <button
          className={`hamburger-btn ${isOpen ? "open" : ""}`}
          onClick={() => setIsOpen(!isOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      )}

      {/* Sidebar overlay - only on mobile when open */}
      {isMobile && isOpen && (
        <div className="sidebar-overlay" onClick={() => setIsOpen(false)} />
      )}

      {/* Sidebar */}
      <aside
        className={`sidebar ${isMobile ? "mobile" : ""} ${isOpen ? "open" : ""}`}
      >
        <div className="sidebar-header">
          <h3 className="sidebar-title">Navigation</h3>
          {isMobile && (
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              ✕
            </button>
          )}
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item, index) => (
            <button
              key={index}
              className={`sidebar-item ${isActive(item.path) ? "active" : ""}`}
              onClick={() => handleItemClick(item.path)}
            >
              <span className="sidebar-icon">{item.icon}</span>
              <span className="sidebar-label">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-status">
            <span className="status-dot online"></span>
            <small>Online</small>
          </div>
        </div>
      </aside>
    </>
  );
}

export default UserSidebar;
