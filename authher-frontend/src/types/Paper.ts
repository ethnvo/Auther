export interface Paper {
  id: any;
  title: string;
  abstract: string;
  authors: string[];
  date: string;
  has_woman_author: boolean | "uncertain";
  link: string;
}
