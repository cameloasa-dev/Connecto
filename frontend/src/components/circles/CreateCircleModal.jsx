// frontend/src/components/circles/CreateCircleModal.jsx

import { useState } from "react";
import PropTypes from "prop-types";
import { useCreateCircle } from "../../hooks/mutations/useCircleMutations";
import "./CreateCircleModal.css";

const CreateCircleModal = ({ isOpen, onClose, onCircleCreated }) => {
  const createCircle = useCreateCircle();

  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });

  const [error, setError] = useState("");

  if (!isOpen) return null;

  const loading = createCircle.isPending;

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setError("");

      const newCircle = await createCircle.mutateAsync(formData);

      onCircleCreated?.(newCircle);

      setFormData({
        name: "",
        description: "",
      });

      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create circle");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Create New Circle</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="circle-name">Circle Name *</label>

            <input
              id="circle-name"
              type="text"
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
              placeholder="Enter circle name"
            />
          </div>

          <div className="form-group">
            <label htmlFor="circle-description">Description</label>

            <textarea
              id="circle-description"
              value={formData.description}
              onChange={(e) =>
                setFormData((prev) => ({
                  ...prev,
                  description: e.target.value,
                }))
              }
              maxLength={255}
              placeholder="What's this circle about?"
              rows={3}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="modal-actions">
            <button type="button" onClick={onClose} disabled={loading}>
              Cancel
            </button>

            <button type="submit" disabled={loading}>
              {loading ? "Creating..." : "Create Circle"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

CreateCircleModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  onCircleCreated: PropTypes.func,
};

export default CreateCircleModal;
