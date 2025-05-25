// src/lib/favorites.ts
import { Paper } from "../types/Paper";

const API = "http://localhost:8000/api/favorites/";

export interface FavRecord {
  id: string;
  paper: Paper;
  created_at?: string;
}

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
}
/**
 * Get the current user’s favorites
 */
export async function fetchFavorites(): Promise<FavRecord[]> {
  const res = await fetch(API, { credentials: "include" });
  if (!res.ok) throw new Error("Failed to load favorites");
  return res.json();
}

/**
 * Add a paper to favorites, returns the created record
 */
export async function addFavorite(paper: Paper): Promise<FavRecord> {
  const res = await fetch(API, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken() || "",
    },
    // send paper_id, matching what your view expects
    body: JSON.stringify({ paper_id: paper.id }),
  });
  if (!res.ok) {
    const text = await res.text();
    console.error("favorite POST failed:", res.status, text);
    throw new Error("Failed to add favorite");
  }
  return res.json();
}

/**
 * Remove a favorite by its favorite-record ID
 */
export async function removeFavorite(favId: string): Promise<void> {
  const res = await fetch(`${API}${favId}/`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!res.ok) {
    const text = await res.text();
    console.error("favorite DELETE failed:", res.status, text);
    throw new Error("Failed to remove favorite");
  }
}
