export interface Paper {
  title: string;
  abstract: string;
  authors: string[];
  date: string;
  has_woman_author: boolean | "uncertain";
  link: string;
}
