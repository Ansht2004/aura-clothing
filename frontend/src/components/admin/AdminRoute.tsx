import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LoadingSpinner } from '../common/LoadingSpinner';

export const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isAdmin, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner fullPage message="Verifying Administrator Privileges..." />;
  }

  if (!isAuthenticated || !isAdmin) {
    return <Navigate to="/auth?redirect=/admin" replace />;
  }

  return <>{children}</>;
};
