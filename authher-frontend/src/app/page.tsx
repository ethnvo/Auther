"use client";

import DarkModeToggle from "../components/DarkModeToggle";
import SearchBar from "../components/SearchBar";
import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function HomePage() {
  const [recentPapers, setRecentPapers] = useState<any[]>([]);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("recentPapers") || "[]");
    setRecentPapers(saved);
  }, []);

  return (
    <div className="relative min-h-screen bg-white dark:bg-black overflow-hidden transition-colors duration-300">
      {/* Gradient overlay */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="h-full w-full bg-gradient-to-t from-rose-300/20  via-stone-100 to-stone-100 dark:from-purple-600/20 dark:via-transparent dark:to-transparent" />
      </div>

      {/* Main content */}
      <div className="relative z-10 px-4 min-h-screen text-black dark:text-white flex flex-col items-center">
        <DarkModeToggle />

        {/* Logo pushed up with top padding */}
        <div className="mt-64">
          <img
            src="/autherlogolight.svg"
            alt="logo"
            className="w-64 scale-150 mb-6 dark:hidden"
          />
          <img
            src="/autherlogodark.svg"
            alt="logo"
            className="w-64 scale-150 mb-6 hidden dark:block"
          />
        </div>
        <p className="text-center text-lg text-gray-600 dark:text-gray-400 max-w-md">
          Start your search with women-led research.
        </p>
        {/* Search bar below with clean spacing */}
        <div className="mt-12 w-full max-w-xl">
          <SearchBar autoFocus placeholder="Search academic topics..." />
        </div>
        {recentPapers.length > 0 && (
          <div className="mt-16 w-full max-w-xl text-left">
            <h3 className="text-md font-semibold mb-2 text-gray-700 dark:text-gray-300">
              Recently Viewed
            </h3>
            <ul className="space-y-3">
              {recentPapers.map((paper, idx) => (
                <li key={idx}>
                  <Link
                    href={paper.link}
                    target="_blank"
                    className="block text-blue-600 dark:text-blue-400 hover:underline"
                  >
                    <p className="font-medium">{paper.title}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {paper.authors?.join(", ")}
                    </p>
                    <p className="text-xs italic">
                      {paper.has_woman_author === true
                        ? "✅ Verified Women-Led"
                        : paper.has_woman_author === false
                          ? "🚫 No woman author"
                          : "❓ Possibly Women Led"}
                    </p>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
