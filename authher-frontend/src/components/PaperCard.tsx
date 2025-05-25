import React from "react";
import { Paper } from "../types/Paper";

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
    <a
      href={paper.link}
      target="_blank"
      rel="noopener noreferrer"
      className="block"
    >
      <div
        className={`
          bg-white dark:bg-gray-800 
          border border-gray-200 dark:border-gray-600 
          rounded-lg shadow 
          p-4 space-y-2 
          transition-colors duration-300
        `}
      >
        <h2 className="text-lg font-bold text-black dark:text-white">
          {paper.title}
        </h2>

        {/* EDIT: Adjust author text styling here */}
        <p className="text-xs text-gray-500 dark:text-gray-400">
          Authors: {paper.authors.join(", ")}
        </p>

        {/* EDIT: Adjust date text styling here */}
        <p className="text-xs text-gray-500 dark:text-gray-400">
          Published: {paper.date}
        </p>

        {/* EDIT: Change tag appearance here */}
        <span className="inline-block text-xs text-blue-600 dark:text-blue-400 font-medium">
          {genderTag()}
        </span>

        {/* EDIT: Tweak abstract styling here */}
        <p className="text-sm text-gray-600 dark:text-gray-300">
          {paper.abstract}
        </p>
      </div>
    </a>
  );
};

export default PaperCard;
