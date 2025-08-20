import React, { useEffect, useState } from "react";
import { getCandidatesByRegion, castVote, getResults } from "../services/api";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function Results() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const res = await getResults();
        setResults(res.data || []);
      } catch (error) {
        console.error("Error fetching results:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, []);

  if (loading) return <p className="p-6 text-white">Loading results...</p>;

  // Sort results by votes (highest first)
  const sortedResults = [...results].sort((a, b) => b.votes - a.votes);

  // Total votes
  const totalVotes = sortedResults.reduce((sum, c) => sum + c.votes, 0);

  // Add percentage share to each candidate
  const resultsWithPercent = sortedResults.map((c) => ({
    ...c,
    percent: totalVotes > 0 ? ((c.votes / totalVotes) * 100).toFixed(2) : 0,
  }));

  // Winner (top candidate)
  const winner = resultsWithPercent.length > 0 ? resultsWithPercent[0] : null;

  return (
    <div className="p-6 bg-gray-900 min-h-screen text-white">
      <h2 className="text-3xl font-bold mb-6">Election Results</h2>

      {resultsWithPercent.length === 0 ? (
        <p className="bg-gray-800 p-4 rounded-lg">No results available yet.</p>
      ) : (
        <div className="space-y-8">
          {/* Winner Highlight */}
          {winner && (
            <div className="bg-green-700 p-6 rounded-xl shadow-lg text-white">
              <h3 className="text-2xl font-bold mb-2">🏆 Winner</h3>
              <p className="text-xl">
                <span className="font-semibold">{winner.name}</span>{" "}
                ({winner.party || "Independent"}) from{" "}
                {winner.region || "N/A"}
              </p>
              <p className="mt-2 text-lg">
                ✅ Total Votes:{" "}
                <span className="font-bold text-yellow-300">
                  {winner.votes} ({winner.percent}%)
                </span>
              </p>
            </div>
          )}

          {/* Results Table */}
          <div className="bg-gray-800 p-6 rounded-xl shadow-lg">
            <table className="w-full border-collapse border border-gray-700">
              <thead>
                <tr className="bg-gray-700">
                  <th className="p-3 text-left">Candidate</th>
                  <th className="p-3 text-left">Party</th>
                  <th className="p-3 text-left">Region</th>
                  <th className="p-3 text-center">Votes</th>
                  <th className="p-3 text-center">Share (%)</th>
                </tr>
              </thead>
              <tbody>
                {resultsWithPercent.map((candidate, index) => (
                  <tr key={index} className="hover:bg-gray-700">
                    <td className="p-3">{candidate.name}</td>
                    <td className="p-3">{candidate.party || "N/A"}</td>
                    <td className="p-3">{candidate.region || "N/A"}</td>
                    <td className="p-3 text-center font-bold">
                      {candidate.votes}
                    </td>
                    <td className="p-3 text-center text-yellow-300">
                      {candidate.percent}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Results Bar Chart */}
          <div className="bg-gray-800 p-6 rounded-xl shadow-lg">
            <h3 className="text-xl font-semibold mb-4">Votes Distribution</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={resultsWithPercent}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="name" stroke="#ccc" />
                <YAxis stroke="#ccc" />
                <Tooltip
                  formatter={(value, name, props) => {
                    if (name === "votes") {
                      return [`${value} (${props.payload.percent}%)`, "Votes"];
                    }
                    return [value, name];
                  }}
                  contentStyle={{ backgroundColor: "#333", color: "#fff" }}
                />
                <Bar dataKey="votes" fill="#4ade80" barSize={50} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

export default Results;
