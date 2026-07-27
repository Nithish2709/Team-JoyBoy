import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../store/useAuthStore';

export default function PublicRoute() {
  const { isAuthenticated } = useAuthStore();

  // If the user is already authenticated, redirect them away from public routes like login
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
}
