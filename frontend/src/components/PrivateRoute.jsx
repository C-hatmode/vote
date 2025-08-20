// src/components/PrivateRoute.jsx
import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const PrivateRoute = ({ children }) => {
  const { voter } = useContext(AuthContext);

  if (!voter) {
    return <Navigate to="/login" />;
  }

  if (!voter.verified) {
    return <Navigate to="/face-auth" />;
  }

  return children;
};

export default PrivateRoute;
