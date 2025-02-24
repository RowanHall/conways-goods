import React, { useState } from "react";
import axios from "axios";
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;
import { useNavigate } from "react-router-dom";
import "./DeletePost.css";

interface DeletePostProps {
  postId: number;
}

const DeletePost: React.FC<DeletePostProps> = ({ postId }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const navigate = useNavigate();

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to delete this post?")) {
      setIsDeleting(true);
      try {
        await axios.delete(`${API_BASE_URL}/api/posts/delete/${postId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        navigate("/shop");
      } catch (error) {
        console.error("Error deleting post:", error);
        alert("Failed to delete post");
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <button
      onClick={handleDelete}
      disabled={isDeleting}
      className="delete-post-button"
    >
      {isDeleting ? "Deleting..." : "DELETE POST"}
    </button>
  );
};

export default DeletePost;
