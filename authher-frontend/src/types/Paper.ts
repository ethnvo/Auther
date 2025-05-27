export interface Paper {
  id: number | string;
  title: string;
  abstract: string;
  authors: string[];
  date: string;
  has_woman_author: boolean | "uncertain" | null;
  link: string;
}
