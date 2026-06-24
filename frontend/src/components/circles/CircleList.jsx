import CircleCard from "./CircleCard";
import PropTypes from "prop-types";
import "./CircleList.css";

const CircleList = ({ circles = [] }) => {
  if (!circles.length) {
    return (
      <div className="empty-state">
        <p>You are not part of any circles yet.</p>
      </div>
    );
  }

  // SORTARE ALFABETICĂ
  const sorted = [...circles].sort((a, b) => a.name.localeCompare(b.name));

  // GRUPARE
  const ownerCircles = sorted.filter((c) => c.role === "owner");
  const memberCircles = sorted.filter((c) => c.role === "member");

  // STATISTICI
  const stats = {
    total: circles.length,
    owners: ownerCircles.length,
    members: memberCircles.length,
    private: circles.filter((c) => c.is_private).length,
    public: circles.filter((c) => !c.is_private).length,
  };

  return (
    <div className="circle-list-container">
      {/* ⭐ STATISTICI */}
      <div className="circle-stats">
        <div className="stat-box">
          <span className="stat-number">{stats.total}</span>
          <span className="stat-label">Total Circles</span>
        </div>

        <div className="stat-box">
          <span className="stat-number">{stats.owners}</span>
          <span className="stat-label">Owned</span>
        </div>

        <div className="stat-box">
          <span className="stat-number">{stats.members}</span>
          <span className="stat-label">Joined</span>
        </div>

        <div className="stat-box">
          <span className="stat-number">{stats.private}</span>
          <span className="stat-label">Private</span>
        </div>

        <div className="stat-box">
          <span className="stat-number">{stats.public}</span>
          <span className="stat-label">Public</span>
        </div>
      </div>

      {/* ⭐ OWNER SECTION */}
      {ownerCircles.length > 0 && (
        <div className="circle-section">
          <h3 className="circle-section-title">Circles You Own</h3>
          <div className="circles-grid">
            {ownerCircles.map((circle) => (
              <CircleCard key={circle.id} circle={circle} />
            ))}
          </div>
        </div>
      )}

      {/* ⭐ MEMBER SECTION */}
      {memberCircles.length > 0 && (
        <div className="circle-section">
          <h3 className="circle-section-title">Circles You Joined</h3>
          <div className="circles-grid">
            {memberCircles.map((circle) => (
              <CircleCard key={circle.id} circle={circle} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

CircleList.propTypes = {
  circles: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      description: PropTypes.string,
      is_private: PropTypes.bool,
      role: PropTypes.string.isRequired,
    }),
  ).isRequired,
};

export default CircleList;
