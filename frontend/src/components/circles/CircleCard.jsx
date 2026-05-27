// frontend/src/components/circles/CircleCard.jsx
// Component for displaying a circle card in the dashboard
import "./CircleCard.css";
const CircleCard = ({ circle, onClick }) => {
  const getBadge = (role) => {
    const badges = {
      owner: "👑",
      moderator: "🛡️",
      member: "👤",
    };
    return badges[role] || "👤";
  };

  return (
    <div className="circle-card" onClick={onClick}>
      <h3>{circle.name}</h3>
      <p>{circle.description || "No description"}</p>
      <div className="circle-meta">
        <span className="badge">{circle.badge || getBadge(circle.role)}</span>
        <span className="role">{circle.role}</span>
        <span className="member-count">{circle.member_count || 0} members</span>
      </div>
    </div>
  );
};

export default CircleCard;
