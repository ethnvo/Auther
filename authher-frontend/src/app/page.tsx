"use client";

import DarkModeToggle from "../components/DarkModeToggle";
import SearchBar from "../components/SearchBar";

export default function HomePage() {
  return (
    <div className="relative min-h-screen bg-white dark:bg-black overflow-hidden transition-colors duration-300">
      {/* Gradient overlay */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <div className="h-full w-full bg-gradient-to-t from-orange-500/20 via-transparent to-transparent dark:from-purple-600/20 dark:via-transparent dark:to-transparent" />
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
      </div>
    </div>
  );
}
