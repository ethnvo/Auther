import React from "react";
import { Paper } from "../types/Paper";

interface PaperCardProps {
  paper: Paper;
}
const PaperCard: React.FC<PaperCardProps> = ({ paper }) => {
  const genderTag = () => {
    if (paper.has_woman_author === true) return "✅ Woman author";
    if (paper.has_woman_author === false) return "🚫 No woman author";
    return "❓ Uncertain";
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow p-4 space-y-2">
      <h2 className="text-lg text-black font-bold">{paper.title}</h2>
      <p className="text-sm text-gray-600">{paper.abstract}</p>
      <p className="text-xs text-gray-500">
        Authors: {paper.authors.join(", ")}
      </p>
      <p className="text-xs text-gray-500">Published: {paper.date}</p>
      <span className="inline-block text-xs text-blue-600 font-medium">
        {genderTag()}
      </span>
      <a
        href={paper.link}
        target="_blank"
        rel="noopener noreferrer"
        className="block text-sm text-indigo-500 underline mt-2"
      >
        View on Semantic Scholar
      </a>
    </div>
  );
};

export default PaperCard;
