"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { fetchPapers } from "../../lib/api";
import { Paper } from "../../types/Paper";
import PaperCard from "../../components/PaperCard";
import SearchBar from "../../components/SearchBar";
import DarkModeToggle from "@/components/DarkModeToggle";
import { AnimatePresence } from "framer-motion";
import SkeletonCard from "@/components/SkeletonCard";
import Link from "next/link";
import { motion } from "framer-motion";

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const query = searchParams?.get("query") ?? "";
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query) return;

    setLoading(true);
    setPapers([]); // 👈 clear old results

    fetchPapers(query)
      .then((data) => {
        setPapers(data);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setPapers([]);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [query]);

  return (
    <div className="relative min-h-screen bg-white dark:bg-black overflow-hidden transition-colors duration-300">
      {/* Gradient overlay */}
      <div className="fixed bottom-0 left-0 w-full h-[40vh] pointer-events-none z-0">
        <div className="h-full w-full bg-gradient-to-t from-orange-400/20 to-transparent dark:from-purple-600/20 dark:to-transparent" />
      </div>

      {/* Page content */}
      <div className="relative z-10 text-black dark:text-white transition-colors duration-300">
        <DarkModeToggle />
        <div className="p-6 w-full max-w-4xl mx-auto space-y-6 items-start text-left">
          <div className="flex items-center gap-4 pl-6 mb-4">
            {/* Logos, scaled  and grouped */}
            <motion.div>
              <div className="flex items-center gap-2 hover:scale-105 transition-all duration-200">
                <Link href="/" className="flex items-center gap-2">
                  <img
                    src="/autherlogolight.svg"
                    alt="Auther Logo Light"
                    className=" dark:hidden"
                  />
                  <img
                    src="/autherlogodark.svg"
                    alt="Auther Logo Dark"
                    className="scale-100 hidden dark:block"
                  />
                </Link>
              </div>
            </motion.div>

            {/* Search bar pushed left to align with cards */}
            <SearchBar initialValue={query} />
          </div>

          {loading && (
            <div className="space-y-4">
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </div>
          )}

          {!loading && papers.length === 0 && (
            <p className="text-center text-sm text-gray-600 dark:text-gray-400">
              No results found for "{query}"
            </p>
          )}
          <div className="space-y-4">
            <AnimatePresence mode="wait">
              {papers.map((paper, i) => (
                <PaperCard key={`${query}-${i}`} paper={paper} />
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
