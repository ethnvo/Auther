"use client";

import { useState, useEffect } from "react";

export default function DarkModeToggle() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") setDarkMode(true);
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  return (
    <div
      className={`absolute top-4 right-4 p-[2px] rounded-full transition-all duration-300 ${
        darkMode
          ? "bg-gradient-to-r to-[#9C56B5]  from-indigo-400"
          : "bg-gradient-to-r from-orange-400 to-pink-500"
      }`}
    >
      <button
        onClick={() => setDarkMode(!darkMode)}
        className={`rounded-full p-2 shadow-md transition-all duration-300
          ${darkMode ? "bg-black text-white" : "bg-white text-black"}`}
        aria-label="Toggle dark mode"
      >
        {darkMode ? "☀️" : "🌙"}
      </button>
    </div>
  );
}
