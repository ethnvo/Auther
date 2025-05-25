"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

interface SearchBarProps {
  initialValue?: string;
  placeholder?: string;
  autoFocus?: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({
  initialValue = "",
  placeholder = "Search...",
  autoFocus = false,
}) => {
  const [term, setTerm] = useState(initialValue);
  const router = useRouter();

  const handleSubmit = () => {
    const trimmed = term.trim();
    if (trimmed) {
      router.push(`/results?query=${encodeURIComponent(trimmed)}`);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div className="w-full max-w-xl flex gap-2">
      <input
        value={term}
        onChange={(e) => setTerm(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder={placeholder}
        autoFocus={autoFocus}
        // EDIT: Adjust input styling here
        className="flex-grow px-4 py-2 text-black dark:text-white bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
      />
      <button
        onClick={handleSubmit}
        // EDIT: Adjust button styling here
        className="bg-indigo-600 text-white px-4 py-2 rounded-lg transition-all duration-300 hover:bg-indigo-700 dark:hover:bg-indigo-500"
      >
        Search
      </button>
    </div>
  );
};

export default SearchBar;
