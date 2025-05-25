"use client";

import { useState } from "react";
import SearchBar from "../components/SearchBar";

export default function HomePage() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div
      className={`${darkMode ? "bg-gray-900 text-white" : "bg-white text-black"} min-h-screen flex flex-col items-center justify-center px-4 transition-colors duration-300`}
    >
      <button
        onClick={() => setDarkMode(!darkMode)}
        className="absolute top-4 right-4 bg-gray-300 dark:bg-gray-700 p-2 rounded-full shadow-md"
      >
        {darkMode ? "☀️" : "🌙"}
      </button>
      <img
        src={darkMode ? `autherlogodark.png` : `autherlogolight.png`}
        alt=""
        className="w-32 mb-6"
      />
      <SearchBar autoFocus placeholder="Search academic topics..." />
    </div>
  );
}
