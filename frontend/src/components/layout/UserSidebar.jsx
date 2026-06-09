// frontend/src/components/layout/UserSidebar.jsx
import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./UserSidebar.css";

function UserSidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const [isOpen, setIsOpen] = useState(window.innerWidth > 768);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth <= 768;
      setIsMobile(mobile);
      setIsOpen(!mobile);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const menuItems = [
    { icon: "🏠", label: "Dashboard", path: "/user-dashboard" },
    { icon: "🔍", label: "Search", path: "/search" },
    { icon: "⚙️", label: "Settings", path: "/settings" },
    { icon: "❓", label: "Help", path: "/help" },
  ];

  const isActive = (path) => location.pathname === path;

  const handleItemClick = (path) => {
    navigate(path);
    if (isMobile) setIsOpen(false);
  };

  return (
    <>
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

      {isMobile && isOpen && (
        <div className="sidebar-overlay" onClick={() => setIsOpen(false)} />
      )}

      <aside className={`sidebar ${isMobile ? "mobile" : ""} ${isOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <h3 className="sidebar-title">Navigation</h3>
          {isMobile && (
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              ✕
            </button>
          )}
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <button
              key={item.path}
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
