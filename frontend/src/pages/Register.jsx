import { useState } from "react";
import { registerVoter } from "../services/api";
import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    aadhaar: "",
    email: "",
    phone: "",
    age: "",
    gender: "",
    assembly_location: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await registerVoter(formData);
      if (res.data.message) {
        navigate("/"); // redirect to login
      } else {
        setError(res.data.error || "Registration failed");
      }
    } catch (err) {
      setError("Something went wrong. Try again.");
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md p-6 bg-white shadow-lg rounded-xl">
        <h2 className="text-2xl font-bold mb-4 text-center">Voter Registration</h2>
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <form onSubmit={handleRegister} className="space-y-3">
          <input type="text" name="name" placeholder="Full Name" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <input type="text" name="aadhaar" placeholder="Aadhaar Number" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <input type="email" name="email" placeholder="Email" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <input type="text" name="phone" placeholder="Phone" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <input type="number" name="age" placeholder="Age" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <select name="gender" onChange={handleChange} required className="w-full p-2 border rounded-md">
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
          <input type="text" name="assembly_location" placeholder="Assembly Location" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <input type="password" name="password" placeholder="Password" onChange={handleChange} required className="w-full p-2 border rounded-md" />
          <button type="submit" className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700">Register</button>
        </form>
        <p className="text-center text-sm mt-3">
          Already have an account?{" "}
          <a href="/" className="text-blue-600 hover:underline">
            Login
          </a>
        </p>
      </div>
    </div>
  );
}

export default Register;
