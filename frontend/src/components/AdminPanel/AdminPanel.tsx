import React from "react";
import CreatePostForm from "../CreatePostForm/CreatePostForm";
import { useAuth } from "../../context/AuthContext";
const AdminPanel = () => {
  const { isAdmin } = useAuth();

  if (!isAdmin) {
    return <div>Access Denied</div>;
  } 

  return (
    <div>
      <h1>ADMIN PANEL</h1>
      <CreatePostForm />
    </div>
  );
};

export default AdminPanel;
