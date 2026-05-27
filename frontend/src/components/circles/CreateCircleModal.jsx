// frontend/src/components/layout/CreateCircleModal.jsx
import { useState } from "react";
import { circleService } from "../../services/circle.service";
import "./CreateCircleModal.css";

const CreateCircleModal = ({ isOpen, onClose, onCircleCreated }) => {
  console.log("📦 CreateCircleModal rendering - isOpen:", isOpen);

  const [formData, setFormData] = useState({
    name: "",
    description: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // If the modal is not open, don't render anything
  if (!isOpen) {
    console.log("🚫 Modal not open - returning null");
    return null;
  }

  console.log("✅ Modal is open - rendering content");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("📝 Form submitted:", formData);

    try {
      setLoading(true);
      setError(null);
      const newCircle = await circleService.createCircle(formData);
      console.log("✅ Circle created successfully:", newCircle);
      onCircleCreated(newCircle);
      onClose();
      setFormData({ name: "", description: "" }); // Reset form
    } catch (err) {
      console.error("❌ Error creating circle:", err);
      setError(err.response?.data?.detail || "Failed to create circle");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h2>Create New Circle</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Circle Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              required
              minLength={3}
              maxLength={50}
              placeholder="Enter circle name"
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              maxLength={255}
              placeholder="What's this circle about? (optional)"
              rows="3"
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

export default CreateCircleModal;
