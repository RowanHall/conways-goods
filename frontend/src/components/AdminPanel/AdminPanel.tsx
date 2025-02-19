import React from 'react';
import CreatePostForm from '../CreatePostForm/CreatePostForm';
import { useAuth } from '../../context/AuthContext';

const AdminPanel = () => {
  const { isAdmin } = useAuth();

  if (!isAdmin) {
    return <div>Access Denied</div>;
  }

  return (
    <div className="admin-panel">
      <h1>Admin Panel</h1>
      <CreatePostForm />
    </div>
  );
};

export default AdminPanel; 