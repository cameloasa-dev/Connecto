// frontend/src/components/layout/navbar/NavbarNotificationsDropdown.jsx
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import "./NavbarNotificationsDropdown.css";

export const NavbarNotificationsDropdown = ({ data, close }) => {
  const navigate = useNavigate();

  if (!data || data.total === 0) {
    return (
      <div className="notif-dropdown">
        <div className="notif-empty">No pending comments</div>
      </div>
    );
  }

  return (
    <div className="notif-dropdown">
      <div className="notif-header">Pending Comments</div>

      {data.circles.map((circle) => (
        <div key={circle.circleId} className="notif-item">
          <div className="notif-circle-name">{circle.circleName}</div>
          <div className="notif-count">{circle.comments.length} pending</div>

          <button
            className="notif-view-btn"
            onClick={() => {
              close();
              navigate(`/circle/${circle.circleId}?tab=pending`);
            }}
          >
            View
          </button>
        </div>
      ))}
    </div>
  );
};

NavbarNotificationsDropdown.propTypes = {
  data: PropTypes.shape({
    total: PropTypes.number.isRequired,
    circles: PropTypes.arrayOf(
      PropTypes.shape({
        circleId: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
          .isRequired,
        circleName: PropTypes.string.isRequired,
        comments: PropTypes.arrayOf(
          PropTypes.shape({
            id: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
              .isRequired,
            post_id: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
              .isRequired,
            content: PropTypes.string.isRequired,
            author: PropTypes.string,
            created_at: PropTypes.string,
          }),
        ).isRequired,
      }),
    ).isRequired,
  }),
  close: PropTypes.func.isRequired,
};
