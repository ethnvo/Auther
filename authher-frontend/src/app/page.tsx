"use client";

import DarkModeToggle from "../components/DarkModeToggle";
import SearchBar from "../components/SearchBar";
import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import GenderTag from "@/components/GenderTag";
import Image from "next/image";

type RecentPaper = {
  title: string;
  link: string;
  authors: string[];
  has_woman_author: boolean | "uncertain" | null;
};

export default function HomePage() {
  const [recentPapers, setRecentPapers] = useState<RecentPaper[]>([]);

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
          <Image
            src="/autherlogolight.svg"
            alt="Auther Logo Light"
            width={256}
            height={256}
            className="scale-150 mb-6 dark:hidden"
          />
          <Image
            src="/autherlogodark.svg"
            alt="Auther Logo Dark"
            width={256}
            height={256}
            className="scale-150 mb-6 hidden dark:block"
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
            <motion.ul
              initial="hidden"
              animate="visible"
              variants={{
                visible: {
                  transition: { staggerChildren: 0.1 },
                },
                hidden: {},
              }}
              className="space-y-3"
            >
              {recentPapers.map((paper, idx) => (
                <motion.li
                  key={idx}
                  variants={{
                    hidden: { opacity: 0, y: 20 },
                    visible: { opacity: 1, y: 0 },
                  }}
                  transition={{ duration: 0.2, ease: "easeOut" }}
                  whileHover={{ scale: 1.03 }}
                >
                  <Link href={paper.link} target="_blank" className="block">
                    <div className="p-3 rounded-md border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 space-y-1 hover:shadow-sm transition">
                      <p className="font-medium text-black dark:text-white">
                        {paper.title}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {paper.authors?.join(", ")}
                      </p>
                      <GenderTag has_woman_author={paper.has_woman_author} />
                    </div>
                  </Link>
                </motion.li>
              ))}
            </motion.ul>
          </div>
        )}
      </div>
    </div>
  );
}
