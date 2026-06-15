//frontend/src/components/posts/PostEditor.jsx
import { useState } from "react";
import propTypes from "prop-types";
import { useUpdateCircle } from "../../hooks/mutations/useCircleMutations";

const CircleEditor = ({ circle, onSuccess, onCancel }) => {
  const [name, setName] = useState(circle.name);
  const [description, setDescription] = useState(circle.description);

  const { mutateAsync: updateCircle, isPending } = useUpdateCircle();

  const handleSave = async () => {
    try {
      if (name === circle.name && description === circle.description) {
        onCancel();
        return;
      }

      await updateCircle({
        circleId: circle.id,
        circleData: { name, description },
      });

      onSuccess();
    } catch (err) {
      console.error("Failed to update circle:", err);
    }
  };
  return (
    <div className="post-editor">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={isPending}
      />

      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={isPending}
      />

      <div className="actions">
        <button
          className="primary-btn"
          onClick={handleSave}
          disabled={isPending}
        >
          Save
        </button>

        <button
          className="secondary-btn"
          onClick={onCancel}
          disabled={isPending}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

CircleEditor.propTypes = {
  circle: propTypes.shape({
    id: propTypes.number.isRequired,
    name: propTypes.string.isRequired,
    description: propTypes.string.isRequired,
  }).isRequired,
  onSuccess: propTypes.func.isRequired,
  onCancel: propTypes.func.isRequired,
};

export default CircleEditor;
