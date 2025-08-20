import React, { useRef, useState, useContext } from "react";
import Webcam from "react-webcam";
import { AuthContext } from "../context/AuthContext";
import { verifyFace } from "../services/api";

const videoConstraints = {
  width: 400,
  height: 300,
  facingMode: "user",
};

function FaceAuth() {
  const webcamRef = useRef(null);
  const { voter, markVerified } = useContext(AuthContext);

  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const capture = async () => {
    if (!webcamRef.current || !voter) {
      setStatus("❌ No voter data or webcam not ready");
      return;
    }

    const imageSrc = webcamRef.current.getScreenshot(); // ✅ Base64 string

    try {
      setLoading(true);
      setStatus("Verifying...");

      // ✅ Use MongoDB _id, not Aadhaar
      await verifyFace(voter._id, imageSrc);

      setStatus("✅ Face verified successfully!");
      setTimeout(() => {
        markVerified();
      }, 1200);
    } catch (error) {
      console.error("❌ Face verification error:", error.response?.data || error.message);
      setStatus("❌ Face verification failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h2 className="text-2xl font-bold mb-4">Face Authentication</h2>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={videoConstraints}
        className="rounded-xl shadow-lg mb-4"
      />
      <button
        onClick={capture}
        disabled={loading}
        className="px-6 py-2 bg-blue-500 rounded-xl hover:bg-blue-600 transition"
      >
        {loading ? "Verifying..." : "Capture & Verify"}
      </button>
      {status && <p className="mt-4">{status}</p>}
    </div>
  );
}

export default FaceAuth;
