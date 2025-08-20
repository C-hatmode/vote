import React, { useEffect, useState, useContext } from "react";
import { getCandidatesByRegion, castVote, getResults } from "../services/api";
import { AuthContext } from "../context/AuthContext";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

function Dashboard() {
  const { voter } = useContext(AuthContext);
  const [candidates, setCandidates] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (voter?.aadhaar) {
      fetchCandidates();
      fetchResults();
    }
  }, [voter]);

  const fetchCandidates = async () => {
    try {
      const res = await getCandidatesByRegion(voter.aadhaar);
      setCandidates(res.data.candidates || []);
    } catch (err) {
      console.error("Error fetching candidates", err);
    }
  };

  const fetchResults = async () => {
    try {
      const res = await getResults();
      // filter results for voter's region only
      const regionalResults = res.data.results.filter(
        (c) => c.region === voter.assembly_location
      );
      setResults(regionalResults);
    } catch (err) {
      console.error("Error fetching results", err);
    } finally {
      setLoading(false);
    }
  };

  const handleVote = async (candidateId) => {
    try {
      await castVote(voter.aadhaar, candidateId);
      alert("Vote cast successfully!");
      fetchCandidates();
      fetchResults(); // refresh live results
    } catch (err) {
      alert("Error casting vote: " + err.response?.data?.error);
    }
  };

  return (
    <div className="p-6">
      {/* Voter Info */}
      <h2 className="text-2xl font-bold mb-4">Welcome, {voter?.name}</h2>
      <p><strong>Aadhaar:</strong> {voter?.aadhaar}</p>
      <p><strong>Region:</strong> {voter?.assembly_location}</p>

      {/* Candidate List */}
      <h3 className="text-xl font-semibold mt-6 mb-2">Candidates in Your Region</h3>
      <ul className="space-y-3">
        {candidates.map((c) => (
          <li
            key={c._id}
            className="border rounded-lg p-3 flex justify-between items-center shadow"
          >
            <div>
              <p className="font-bold">{c.name} ({c.party})</p>
              <p className="text-sm text-gray-600">Votes: {c.votes}</p>
            </div>
            {!voter?.has_voted && (
              <button
                className="bg-blue-600 text-white px-4 py-1 rounded"
                onClick={() => handleVote(c._id)}
              >
                Vote
              </button>
            )}
          </li>
        ))}
      </ul>

      {/* Live Results */}
      <h3 className="text-xl font-semibold mt-8 mb-2">Live Results (Your Region)</h3>
      {loading ? (
        <p>Loading results...</p>
      ) : results.length === 0 ? (
        <p>No results available yet.</p>
      ) : (
        <div className="bg-white p-4 rounded shadow">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={results}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="votes" fill="#2563eb">
                {results.map((entry, index) => (
                  <Cell key={`cell-${index}`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          {/* Percentages */}
          <table className="w-full mt-4 border">
            <thead>
              <tr className="bg-gray-200">
                <th className="p-2">Candidate</th>
                <th className="p-2">Votes</th>
                <th className="p-2">Percentage</th>
              </tr>
            </thead>
            <tbody>
              {results.map((c) => {
                const totalVotes = results.reduce((sum, r) => sum + r.votes, 0);
                const percentage = totalVotes ? ((c.votes / totalVotes) * 100).toFixed(2) : 0;
                return (
                  <tr key={c._id} className="border-t">
                    <td className="p-2">{c.name}</td>
                    <td className="p-2">{c.votes}</td>
                    <td className="p-2">{percentage}%</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
