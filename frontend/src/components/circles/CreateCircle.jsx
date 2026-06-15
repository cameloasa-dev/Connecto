// frontend/src/components/circles/CreateCircle.jsx

import { useState } from "react";
import propTypes from "prop-types";
import { useCreateCircle } from "../../hooks/mutations/useCircleMutations";

const CreateCircle = ({ onCircleCreated }) => {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });

  const { mutate, isPending, error } = useCreateCircle();

  const resetForm = () => {
    setFormData({
      name: "",
      description: "",
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    mutate(formData, {
      onSuccess: (newCircle) => {
        onCircleCreated?.(newCircle);
        resetForm();
      },
    });
  };

  return (
    <form onSubmit={handleSubmit} className="create-circle-form">
      <h3>Create New Circle</h3>

      {error && (
        <div className="error-message">
          {error?.response?.data?.detail || "Failed to create circle"}
        </div>
      )}

      <div className="form-group">
        <input
          type="text"
          placeholder="Circle name"
          value={formData.name}
          onChange={(e) =>
            setFormData((prev) => ({
              ...prev,
              name: e.target.value,
            }))
          }
          required
          minLength={3}
          maxLength={50}
          disabled={isPending}
        />
      </div>

      <div className="form-group">
        <textarea
          placeholder="Describe your circle"
          value={formData.description}
          onChange={(e) =>
            setFormData((prev) => ({
              ...prev,
              description: e.target.value,
            }))
          }
          rows={3}
          maxLength={255}
          disabled={isPending}
        />
      </div>

      <button type="submit" className="primary-btn" disabled={isPending}>
        {isPending ? "Creating..." : "Create Circle"}
      </button>
    </form>
  );
};

CreateCircle.propTypes = {
  onCircleCreated: propTypes.func,
};

export default CreateCircle;
