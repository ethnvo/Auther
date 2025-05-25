import React from "react";
import { Paper } from "../types/Paper";
import { useCallback } from "react";

import { motion } from "framer-motion";

interface PaperCardProps {
  paper: Paper;
}

const PaperCard: React.FC<PaperCardProps> = ({ paper }) => {
  const genderTag = () => {
    if (paper.has_woman_author === true) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-700 dark:bg-[#9C56B5]/20 dark:text-[#9C56B5]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-3 h-3"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
          Verified Women-Led
        </span>
      );
    }

    if (
      paper.has_woman_author === null ||
      paper.has_woman_author === undefined
    ) {
      return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-700 dark:bg-[#9C56B5]/10 dark:text-[#9C56B5]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="w-3 h-3"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4l3 3"
            />
          </svg>
          Possibly Women-Led
        </span>
      );
    }

    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-600 dark:bg-gray-700/30 dark:text-gray-300">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-3 h-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
        Unverified
      </span>
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
    >
      <a
        href={paper.link}
        target="_blank"
        rel="noopener noreferrer"
        className="block"
        onClick={() => {
          try {
            const existing = JSON.parse(
              localStorage.getItem("recentPapers") || "[]"
            );
            const compact = {
              title: paper.title,
              link: paper.link,
              authors: paper.authors,
              has_woman_author: paper.has_woman_author,
            };
            const updated = [
              compact,
              ...existing.filter((p: any) => p.link !== paper.link),
            ].slice(0, 5);
            localStorage.setItem("recentPapers", JSON.stringify(updated));
          } catch (e) {
            console.error("Failed to save recent paper:", e);
          }
        }}
      >
        <div
          className="font-sans rounded-xl p-4 space-y-2 transition-all duration-300 hover:shadow-md hover:scale-[1.01] transform 
             bg-gradient-to-br from-slate-50 to-white 
             dark:from-gray-900 dark:to-black 
             border border-gray-200 dark:border-gray-700"
        >
          <h2 className="text-lg font-bold text-black dark:text-white">
            {paper.title}
          </h2>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Authors: {paper.authors.join(", ")}
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Published: {paper.date}
          </p>
          {genderTag()}

          <p className="text-sm text-gray-600 dark:text-gray-300">
            {paper.abstract}
          </p>
        </div>
      </a>
    </motion.div>
  );
};

export default PaperCard;
