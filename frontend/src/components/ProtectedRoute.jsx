// src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { voter } = useAuth();

  // ❌ If not logged in
  if (!voter) {
    return <Navigate to="/" replace />;
  }

  // ❌ If not face verified yet
  if (!voter.verified) {
    return <Navigate to="/face-auth" replace />;
  }

  // ✅ Access granted
  return children;
};

export default ProtectedRoute;
