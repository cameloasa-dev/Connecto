import { useState } from "react";
import { useNavigate } from "react-router-dom";
import propTypes from "prop-types";
import CircleEditor from "./CircleEditor";
import { useDeleteCircle } from "../../hooks/mutations/useCircleMutations";
import "./CircleCard.css";

const CircleCard = ({ circle }) => {
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);

  const { mutateAsync: deleteCircle, isPending } = useDeleteCircle();

  const handleDelete = async (e) => {
    e.stopPropagation();
    if (isPending) return;
    if (!window.confirm("Delete circle?")) return;

    await deleteCircle(circle.id);
  };

  const openCircle = () => {
    navigate(`/circles/${circle.id}`);
  };

  const closeEditor = () => setIsEditing(false);

  return (
    <div className="circle-card" onClick={openCircle}>
      <div className="circle-content">
        <h4>{circle.name}</h4>
        <p>{circle.description}</p>
      </div>

      <div className="circle-actions">
        <button
          className="circle-action-btn"
          onClick={(e) => {
            e.stopPropagation();
            setIsEditing(true);
          }}
          disabled={isPending}
        >
          Edit
        </button>

        <button
          className="post-action-btn danger"
          onClick={handleDelete}
          disabled={isPending}
        >
          {isPending ? "Deleting..." : "Delete"}
        </button>
      </div>

      {isEditing && (
        <div className="circle-editor-overlay">
          <div className="circle-editor-modal">
            <h3>Edit Circle</h3>

            <CircleEditor
              circle={circle}
              onSuccess={closeEditor}
              onCancel={closeEditor}
            />
          </div>
        </div>
      )}
    </div>
  );
};

CircleCard.propTypes = {
  circle: propTypes.shape({
    id: propTypes.number.isRequired,
    name: propTypes.string.isRequired,
    description: propTypes.string,
  }).isRequired,
};

export default CircleCard;
