// frontend/src/components/circles/CircleList.jsx
import CircleCard from "./CircleCard";
import propTypes from "prop-types";

const CircleList = ({ circles = [] }) => {
  if (!circles.length) {
    return <p className="empty-message">No circles yet.</p>;
  }

  return (
    <div className="circles-feed">
      {circles.map((circle) => (
        <CircleCard key={circle.id} circle={circle} />
      ))}
    </div>
  );
};

CircleList.propTypes = {
  circles: propTypes.arrayOf(
    propTypes.shape({
      id: propTypes.number.isRequired,
      name: propTypes.string.isRequired,
      description: propTypes.string.isRequired,
    }),
  ).isRequired,
};

export default CircleList;
