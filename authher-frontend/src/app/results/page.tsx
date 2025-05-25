"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { fetchPapers } from "../../lib/api";
import { Paper } from "../../types/Paper";
import PaperCard from "../../components/PaperCard";
import SearchBar from "../../components/SearchBar";
import DarkModeToggle from "@/components/DarkModeToggle";

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const query = searchParams?.get("query") ?? "";
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) return;
    setLoading(true);
    fetchPapers(query)
      .then(setPapers)
      .catch(() => setPapers([]))
      .finally(() => setLoading(false));
  }, [query]);

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-black dark:text-white transition-colors duration-300">
      <DarkModeToggle />
      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <SearchBar initialValue={query} />
        {loading && <p>Loading...</p>}
        {!loading && papers.length === 0 && (
          <p>No results found for "{query}"</p>
        )}
        <div className="space-y-4">
          {papers.map((paper, i) => (
            <PaperCard key={i} paper={paper} />
          ))}
        </div>
      </div>
    </div>
  );
}
