import { Paper } from "../types/Paper";

type RawPaper = Omit<Paper, "has_woman_author"> & {
  has_woman_author: boolean | "uncertain" | null | undefined;
};

export async function fetchPapers(search: string): Promise<Paper[]> {
  const res = await fetch(
    `http://127.0.0.1:8000/api/papers/?search=${encodeURIComponent(search)}`
  );

  if (!res.ok) {
    throw new Error(`Failed to fetch papers: ${res.status}`);
  }
  const data: RawPaper[] = await res.json();

  // Normalize has_woman_author (in case it's a boolean or string)
  return data.map((paper) => ({
    ...paper,
    has_woman_author:
      typeof paper.has_woman_author === "boolean"
        ? paper.has_woman_author
        : (paper.has_woman_author as "uncertain"),
  }));
}
