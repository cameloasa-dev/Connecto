// frontend/src/components/circles/CircleSettings.jsx
import { useState } from "react";
import { circleMemberService } from "../../services/circleMember.service";
import { useCirclePermissions } from "../../hooks/useCirclePermissions";
import "./CircleSettings.css";

const CircleSettings = ({ circle, onCircleUpdated }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [newName, setNewName] = useState(circle.name);
  const [loading, setLoading] = useState(false);
  const { canChangeSettings } = useCirclePermissions(circle);

  const handleSaveName = async () => {
    if (newName === circle.name) {
      setIsEditing(false);
      return;
    }

    setLoading(true);
    try {
      const updated = await circleMemberService.updateCircleName(
        circle.id,
        newName,
      );
      onCircleUpdated(updated);
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update circle name:", error);
    } finally {
      setLoading(false);
    }
  };

  if (!canChangeSettings) return null;

  return (
    <div className="circle-settings">
      <h3>Circle Settings</h3>

      <div className="setting-item">
        <label>Circle Name</label>
        {isEditing ? (
          <div className="edit-name">
            <input
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

export default CircleSettings;
