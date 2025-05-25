import React from "react";
import { Paper } from "../types/Paper";
import { useCallback } from "react";

import { motion } from "framer-motion";

interface PaperCardProps {
  paper: Paper;
}

const PaperCard: React.FC<PaperCardProps> = ({ paper }) => {
  const genderTag = () => {
    if (paper.has_woman_author === true) return "✅ Verified Women-Led";
    if (paper.has_woman_author === false) return "🚫 No woman author";
    return "❓ Possibly Women Led";
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
        <div className="font-sans bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-lg shadow p-4 space-y-2 transition-all duration-300 hover:shadow-lg hover:scale-[1.02] transform ">
          <h2 className="text-lg font-bold text-black dark:text-white">
            {paper.title}
          </h2>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Authors: {paper.authors.join(", ")}
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Published: {paper.date}
          </p>
          <span className="inline-block text-xs text-blue-600 dark:text-blue-400 font-medium">
            {genderTag()}
          </span>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            {paper.abstract}
          </p>
        </div>
      </a>
    </motion.div>
  );
};

export default PaperCard;
