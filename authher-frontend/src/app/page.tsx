"use client";

import { useEffect, useState } from "react";
import { fetchPapers } from "../lib/api";
import { Paper } from "../types/Paper";
import PaperCard from "../components/PaperCard";

export default function HomePage() {
  const [searchTerm, setSearchTerm] = useState("esports");
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    if (!searchTerm.trim()) return;
    setLoading(true);
    setError("");
    try {
      const results = await fetchPapers(searchTerm);
      setPapers(results);
    } catch (err) {
      setError("Failed to fetch papers");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    handleSearch();
  }, []);

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-center">Auther</h1>

      <div className="flex flex-col sm:flex-row gap-2">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Enter a topic (e.g. AI, medicine, ethics)"
          className="flex-grow px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          onClick={handleSearch}
          className="bg-indigo-600 text-black px-4 py-2 rounded-md hover:bg-indigo-700"
        >
          Search
        </button>
      </div>

      {loading && <p className="text-gray-600">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && papers.length > 0 && (
        <p className="text-sm text-gray-500">
          Showing {papers.length} result{papers.length > 1 ? "s" : ""}
        </p>
      )}

      {!loading && !error && papers.length === 0 && (
        <p className="text-gray-500 italic">
          No results found for "{searchTerm}".
        </p>
      )}

      <div className="space-y-4">
        {papers.map((paper, i) => (
          <PaperCard key={i} paper={paper} />
        ))}
      </div>
    </div>
  );
}
