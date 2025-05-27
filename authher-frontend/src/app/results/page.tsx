"use client";

import { Suspense } from "react";
import ResultsContent from "./ResultsContent";
import SkeletonCard from "@/components/SkeletonCard";

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="p-6 space-y-4 max-w-4xl mx-auto">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
