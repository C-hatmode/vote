// src/services/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:5002", // root backend URL
});

// ✅ Attach JWT automatically
API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// =======================
// Voter Authentication
// =======================
export const registerVoter = (formData) => API.post("/voter/register", formData);

export const loginVoter = (credentials) => API.post("/voter/login", credentials);

export const getVoter = (aadhaar) => API.get(`/voter/aadhaar/${aadhaar}`);

export const updateVoter = (aadhaar, updates) =>
  API.put(`/voter/update/${aadhaar}`, updates);

// =======================
// Face Authentication
// =======================
export const verifyFace = (aadhaar, imageBase64) => {
  return API.post(
    "/voter/verify_face",
    {
      aadhaar: aadhaar,   // ✅ send Aadhaar, not voter_id
      image: imageBase64, // ✅ base64 string from webcam
    },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
};


// =======================
// Voting & Results
// =======================

// ✅ Fetch candidates by region (assembly_location)
export const getCandidatesByRegion = (region) =>
  API.get(`/candidates/region/${region}`);

// ✅ Cast a vote
export const castVote = (aadhaar, candidateId) =>
  API.post("/vote", { aadhaar, candidate_id: candidateId });

// ✅ Fetch election results
export const getResults = () => API.get("/results");
