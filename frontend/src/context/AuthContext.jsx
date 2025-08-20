// src/context/AuthContext.js
import { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

// ✅ Export AuthContext
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [voter, setVoter] = useState(null);
  const navigate = useNavigate();

  // ✅ Load voter from localStorage on refresh
  useEffect(() => {
    const stored = localStorage.getItem("voter");
    if (stored) {
      setVoter(JSON.parse(stored));
    }
  }, []);

  // ✅ Login (Aadhaar + Password step only)
  const login = (voterData) => {
    const newVoter = { ...voterData, verified: false }; // start as NOT face-verified
    setVoter(newVoter);
    localStorage.setItem("voter", JSON.stringify(newVoter));
    navigate("/face-auth"); // redirect to face authentication
  };

  // ✅ Mark as verified after FaceAuth
  const markVerified = () => {
    if (!voter) return;
    const verifiedVoter = { ...voter, verified: true };
    setVoter(verifiedVoter);
    localStorage.setItem("voter", JSON.stringify(verifiedVoter));
    navigate("/dashboard"); // go to dashboard after success
  };

  // ✅ Logout
  const logout = () => {
    setVoter(null);
    localStorage.removeItem("voter");
    navigate("/");
  };

  return (
    <AuthContext.Provider
      value={{
        voter,               // full voter object { aadhaar, name, verified }
        isFaceVerified: voter?.verified || false, // helper flag
        login,
        logout,
        markVerified,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// ✅ Optional helper hook
export const useAuth = () => useContext(AuthContext);
