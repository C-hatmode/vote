// src/pages/Login.jsx
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { loginVoter } from "../services/api";
import { AuthContext } from "../context/AuthContext";

function Login() {
  const [aadhaar, setAadhaar] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const { setVoter } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await loginVoter({ aadhaar, password });

      // 🔍 Debug: log full response from backend
      console.log("Login API response:", res.data);

      if (res.data.token) {
        // ✅ Save JWT
        localStorage.setItem("token", res.data.token);

        // ✅ Save Aadhaar in context for face verification step
        setVoter({ aadhaar, token: res.data.token, verified: false });

        // ✅ Redirect to Face Authentication
        navigate("/face-auth");
      } else {
        setError("Login failed: No token received");
      }
    } catch (err) {
      console.error("Login error:", err.response || err.message);
      setError(err.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white">
      <form
        onSubmit={handleLogin}
        className="bg-gray-800 p-6 rounded-xl shadow-md w-96"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Voter Login</h2>

        <input
          type="text"
          placeholder="Aadhaar Number"
          value={aadhaar}
          onChange={(e) => setAadhaar(e.target.value)}
          className="w-full mb-3 p-2 rounded bg-gray-700"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-3 p-2 rounded bg-gray-700"
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-600 py-2 rounded"
        >
          Login
        </button>

        {error && <p className="text-red-400 mt-2">{error}</p>}
      </form>
    </div>
  );
}

export default Login;
