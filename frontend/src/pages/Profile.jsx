import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { getVoter, updateVoter } from "../services/api";

function Profile() {
  const { voter } = useContext(AuthContext);
  const [voterInfo, setVoterInfo] = useState(null);
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchVoterInfo = async () => {
      try {
        const res = await getVoter(voter.aadhaar);
        setVoterInfo(res.data);
        setFormData(res.data);
      } catch (error) {
        console.error("Error fetching voter info:", error);
      }
    };
    fetchVoterInfo();
  }, [voter.aadhaar]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await updateVoter(voter.aadhaar, formData);
      setMessage("✅ Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
      setMessage("❌ Failed to update profile.");
    }
  };

  if (!voterInfo) return <p className="p-6 text-white">Loading...</p>;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <h2 className="text-3xl font-bold mb-6">Your Profile</h2>

      <form
        onSubmit={handleUpdate}
        className="bg-gray-800 p-6 rounded-xl shadow-lg space-y-4"
      >
        <div>
          <label className="block text-sm font-medium mb-1">Name</label>
          <input
            type="text"
            name="name"
            value={formData.name || ""}
            onChange={handleChange}
            className="w-full px-3 py-2 rounded-lg text-black"
            disabled
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Aadhaar</label>
          <input
            type="text"
            name="aadhaar"
            value={formData.aadhaar || ""}
            className="w-full px-3 py-2 rounded-lg text-black"
            disabled
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email || ""}
            onChange={handleChange}
            className="w-full px-3 py-2 rounded-lg text-black"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Assembly Location</label>
          <input
            type="text"
            name="assembly_location"
            value={formData.assembly_location || ""}
            onChange={handleChange}
            className="w-full px-3 py-2 rounded-lg text-black"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input
            type="password"
            name="password"
            placeholder="Enter new password (optional)"
            onChange={handleChange}
            className="w-full px-3 py-2 rounded-lg text-black"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 py-2 px-4 rounded-lg hover:bg-blue-600 transition"
        >
          Update Profile
        </button>
      </form>

      {message && (
        <p className="mt-4 p-3 bg-gray-700 rounded-lg text-center">{message}</p>
      )}
    </div>
  );
}

export default Profile;
