import { useState } from "react";
import PropTypes from "prop-types";
import { useCirclePermissions } from "../../hooks/useCirclePermissions";
import { useUpdateCircleName } from "../../hooks/mutations/useCircleMutations";
import "./CircleSettings.css";

const CircleSettings = ({ circle, onCircleUpdated }) => {
  const { canChangeSettings } = useCirclePermissions(circle);

  const updateCircleName = useUpdateCircleName();

  const [isEditing, setIsEditing] = useState(false);
  const [newName, setNewName] = useState(circle.name);

  if (!canChangeSettings) return null;

  const loading = updateCircleName.isPending;

  const handleSaveName = async () => {
    if (newName.trim() === circle.name) {
      setIsEditing(false);
      return;
    }

    try {
      const updatedCircle = await updateCircleName.mutateAsync({
        circleId: circle.id,
        name: newName,
      });

      onCircleUpdated?.(updatedCircle);

      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update circle name:", error);
    }
  };

  return (
    <div className="circle-settings">
      <h3>Circle Settings</h3>

      <div className="setting-item">
        <label htmlFor="circle-name-input">Circle Name</label>

        {isEditing ? (
          <div className="edit-name">
            <input
              id="circle-name-input"
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              minLength={3}
              maxLength={50}
              disabled={loading}
            />

            <button onClick={handleSaveName} disabled={loading}>
              Save
            </button>

            <button onClick={() => setIsEditing(false)} disabled={loading}>
              Cancel
            </button>
          </div>
        ) : (
          <div className="display-name">
            <span>{circle.name}</span>

            <button onClick={() => setIsEditing(true)}>Edit</button>
          </div>
        )}
      </div>
    </div>
  );
};

CircleSettings.propTypes = {
  circle: PropTypes.object.isRequired,
  onCircleUpdated: PropTypes.func,
};

export default CircleSettings;
