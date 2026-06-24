import { useState } from "react";
import propTypes from "prop-types";
import {
  useCreateCircle,
  useUpdateCircle,
} from "../../hooks/mutations/useCircleMutations";

const CircleEditor = ({ circle, onSuccess, onCancel }) => {
  const isEdit = !!circle;

  const [name, setName] = useState(circle?.name || "");
  const [description, setDescription] = useState(circle?.description || "");
  const [isPrivate, setIsPrivate] = useState(circle?.is_private || false);

  const { mutateAsync: createCircle, isPending: isCreating } =
    useCreateCircle();
  const { mutateAsync: updateCircle, isPending: isUpdating } =
    useUpdateCircle();

  const isPending = isCreating || isUpdating;

  const handleSave = async () => {
    try {
      if (isEdit) {
        // nothing changed?
        if (
          name === circle.name &&
          description === circle.description &&
          isPrivate === circle.is_private
        ) {
          onCancel();
          return;
        }

        await updateCircle({
          circleId: circle.id,
          circleData: { name, description, is_private: isPrivate },
        });
      } else {
        await createCircle({
          name,
          description,
          is_private: isPrivate,
        });
      }

      onSuccess();
    } catch (err) {
      console.error("Failed to save circle:", err);
    }
  };

  return (
    <div className="circle-editor">
      <h3>{isEdit ? "Edit Circle" : "Create Circle"}</h3>

      <input
        type="text"
        placeholder="Circle name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={isPending}
      />

      <textarea
        placeholder="Describe your circle"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={isPending}
      />

      <label className="checkbox-row">
        <input
          type="checkbox"
          checked={isPrivate}
          onChange={(e) => setIsPrivate(e.target.checked)}
          disabled={isPending}
        />
        Private circle
      </label>

      <div className="actions">
        <button
          className="primary-btn"
          onClick={handleSave}
          disabled={isPending}
        >
          {isPending ? "Saving..." : "Save"}
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
    id: propTypes.number,
    name: propTypes.string,
    description: propTypes.string,
    is_private: propTypes.bool,
  }),
  onSuccess: propTypes.func.isRequired,
  onCancel: propTypes.func.isRequired,
};

export default CircleEditor;
