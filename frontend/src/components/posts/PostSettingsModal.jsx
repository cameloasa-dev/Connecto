//fronttend/src/components/posts/PostSettingsModal.jsx
import propTypes from "prop-types";
import PostEditor from "./PostEditor";

const PostSettingsModal = ({ post, onClose }) => {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>Edit Post</h3>

        <PostEditor
          post={post}
          onSuccess={onClose}
          onCancel={onClose}
        />
      </div>
    </div>
  );
};

PostSettingsModal.propTypes = {
  post: propTypes.object.isRequired,
  onClose: propTypes.func.isRequired,
};

export default PostSettingsModal;