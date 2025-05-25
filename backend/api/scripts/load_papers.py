# api/scripts/load_papers.py
import time
import requests
from django.core.cache import cache
from api.utils.resolve_author_gender import resolve_author_gender
from api.utils.common_female_names import FEMALE_NAMES

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_PAPER  = "https://api.semanticscholar.org/graph/v1/paper"
OPENALEX_WORKS          = "https://api.openalex.org/works"
GENDERIZE_API           = "https://api.genderize.io"

DEFAULT_LIMIT       = 15
MAX_GENDERIZE_CALLS = 5
CACHE_TTL           = 60 * 60  # 1 hour
MIN_RESULTS         = 2        # hard-coded floor


# ───────────────────────── helper: expand initials ──────────────────────────
def _expand_authors(paper_id: str, external_ids: dict, raw_authors: list[dict]) -> list[dict]:
    cache_key = f"authors_expanded:{paper_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    authors = raw_authors

    # 1) Semantic Scholar detail 
    if all(len(a["name"].split()[0]) <= 2 for a in authors) and paper_id:
        det = requests.get(
            f"{SEMANTIC_SCHOLAR_PAPER}/{paper_id}",
            params={"fields": "authors"},
            timeout=5,
        )
        if det.ok:
            expanded = [
                {"name": au["author"]["name"], "authorId": au["author"]["authorId"]}
                for au in (det.json().get("authors") or [])
                if au.get("author", {}).get("name")
            ]
            if expanded:
                authors = expanded

    # 2) OpenAlex fallback
    if all(len(a["name"].split()[0]) <= 2 for a in authors):
        doi = external_ids.get("DOI")
        if doi:
            oax = requests.get(f"{OPENALEX_WORKS}/doi:{doi}", timeout=5)
            if oax.ok:
                expanded = [
                    {"name": au["author"]["display_name"], "authorId": None}
                    for au in (oax.json().get("authorships") or [])
                    if au.get("author", {}).get("display_name")
                ]
                if expanded:
                    authors = expanded

    if authors:                      # only cache non-empty result
        cache.set(cache_key, authors, CACHE_TTL)
    return authors


# ───────────────────────── helper: resilient search ─────────────────────────
def _semantic_search(query: str, limit: int):
    params = {
        "query":  query,
        "limit":  limit,
        "fields": "title,abstract,authors,year,paperId,externalIds",
    }

    def _call():
        try:
            r = requests.get(SEMANTIC_SCHOLAR_SEARCH, params=params, timeout=10)
            if r.ok:
                return r.json().get("data", []) or []
        except requests.RequestException:
            pass
        return []

    data = _call()
    if data:
        return data
    time.sleep(0.5)          # retry once on empty/failed
    return _call()


# ───────────────────────── main public function ─────────────────────────────
def fetch_and_filter(
    query: str,
    only_women: bool = False,
    year: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> list[dict]:

    papers = _semantic_search(query, limit)
    results: list[dict] = []
    authorless_candidates: list[dict] = []   # store rows with no authors

    # ── main loop ───────────────────────────────────────────────────────────
    for p in papers:
        title       = (p.get("title") or "").strip()
        abstract    = p.get("abstract") or "No abstract available."
        raw_authors = p.get("authors") or []
        year_val    = p.get("year")
        paper_id    = p.get("paperId")
        externalIds = p.get("externalIds", {})

        if year and str(year_val) != str(year):
            continue

        if not raw_authors:
            authorless_candidates.append(p)
            continue

        # quick gender pass
        has_woman = gender_possible = False
        for a in raw_authors:
            first = a["name"].split()[0].lower()
            if first in FEMALE_NAMES:
                has_woman = gender_possible = True
                break
            aid = a.get("authorId")
            if aid:
                gi = resolve_author_gender(aid)
                if gi:
                    gender_possible = True
                    if gi["gender"] == "female":
                        has_woman = True
                        break

        # expand initials if still uncertain
        authors_exp = raw_authors
        if (
            not gender_possible
            and all(len(a["name"].split()[0]) <= 2 for a in raw_authors)
        ):
            authors_exp = _expand_authors(paper_id, externalIds, raw_authors)

        if authors_exp is not raw_authors:
            has_woman = gender_possible = False
            for a in authors_exp:
                first = a["name"].split()[0].lower()
                if first in FEMALE_NAMES:
                    has_woman = gender_possible = True
                    break
                aid = a.get("authorId")
                if aid:
                    gi = resolve_author_gender(aid)
                    if gi:
                        gender_possible = True
                        if gi["gender"] == "female":
                            has_woman = True
                            break

        # Genderize fallback (capped)
        if not has_woman and not gender_possible:
            calls = 0
            for a in authors_exp:
                first = a["name"].split()[0]
                if first.isalpha() and len(first) > 2 and calls < MAX_GENDERIZE_CALLS:
                    calls += 1
                    try:
                        gr = requests.get(GENDERIZE_API, params={"name": first}, timeout=5)
                        if gr.ok and gr.json().get("gender"):
                            gender_possible = True
                            if gr.json()["gender"] == "female":
                                has_woman = True
                                break
                    except requests.RequestException:
                        pass

        if gender_possible and not has_woman:
            continue
        if only_women and not has_woman:
            continue

        link = (
            f"https://www.semanticscholar.org/paper/{paper_id}"
            if paper_id
            else f"https://www.google.com/search?q={title.replace(' ', '+')}"
        )

        results.append(
            {
                "title":            title or "Untitled",
                "abstract":         abstract,
                "authors":          [a["name"] for a in authors_exp],
                "date":             f"{year_val}-01-01" if year_val else None,
                "has_woman_author": True if has_woman else "uncertain",
                "link":             link,
            }
        )

    # ── ensure at least MIN_RESULTS ─────────────────────────────────────────
    if len(results) < MIN_RESULTS:
        already = {r["link"] for r in results}
        for p in papers + authorless_candidates:
            if len(results) >= MIN_RESULTS:
                break
            fallback_link = (
                f"https://www.semanticscholar.org/paper/{p.get('paperId')}"
                if p.get("paperId")
                else f"https://www.google.com/search?q={(p.get('title') or '').replace(' ', '+')}"
            )
            if fallback_link in already:
                continue
            results.append(
                {
                    "title":    (p.get("title") or "").strip() or "Untitled",
                    "abstract": p.get("abstract") or "No abstract available.",
                    "authors":  [a["name"] for a in (p.get("authors") or [])],
                    "date":     f"{p.get('year')}-01-01" if p.get("year") else None,
                    "has_woman_author": False,
                    "link":     fallback_link,
                }
            )
            already.add(fallback_link)

    # final placeholder if everything failed
    if not results:
        results.append(
            {
                "title": "No matching papers found",
                "abstract": "Try a more specific search term.",
                "authors": [],
                "date": None,
                "has_woman_author": False,
                "link": f"https://www.google.com/search?q={query.replace(' ', '+')}",
            }
        )

    return results
