# api/scripts/load_papers.py

import requests
from django.core.cache import cache
from api.utils.resolve_author_gender import resolve_author_gender
from api.utils.common_female_names import FEMALE_NAMES

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_PAPER  = "https://api.semanticscholar.org/graph/v1/paper"
OPENALEX_WORKS         = "https://api.openalex.org/works"
GENDERIZE_API          = "https://api.genderize.io"

DEFAULT_LIMIT       = 10
MAX_GENDERIZE_CALLS = 3       # lower cap for speed
CACHE_TTL           = 60 * 60 # cache expansions 1hr

def _expand_authors(paper_id: str, external_ids: dict, raw_authors: list[dict]) -> list[dict]:
    """
    If all authors are initials, expand via SS detail → OpenAlex,
    and cache by paper_id for CACHE_TTL seconds.
    """
    cache_key = f"authors_expanded:{paper_id}"
    authors = cache.get(cache_key)
    if authors is not None:
        return authors

    authors = raw_authors
    # 1) Semantic Scholar detail
    if all(len(a["name"].split()[0]) <= 2 for a in authors) and paper_id:
         det = requests.get(
             f"{SEMANTIC_SCHOLAR_PAPER}/{paper_id}",
             params={"fields": "authors"},
             timeout=5
         )
         if det.ok:
             ss_auths = det.json().get("authors", []) or []
             expanded = []
             for entry in ss_auths:
                 author_data = entry.get("author") or {}
                 name = author_data.get("name")
                 if not name:
                     continue
                 expanded.append({
                     "name":     name,
                     "authorId": author_data.get("authorId")
                 })
             if expanded:
                 authors = expanded

    if all(len(a["name"].split()[0]) <= 2 for a in authors):
        doi = external_ids.get("DOI")
        if doi:
            oax = requests.get(f"{OPENALEX_WORKS}/doi:{doi}", timeout=5)
            if oax.ok:
                auths = oax.json().get("authorships", [])  # <-- default to empty list
                expanded = []
                for entry in auths:
                    author_info = entry.get("author") or {}
                    disp_name   = author_info.get("display_name")
                    if disp_name:
                        expanded.append({
                            "name":     disp_name,
                            "authorId": None
                        })
                # only overwrite if we actually fetched full names
                if expanded:
                    authors = expanded

    cache.set(cache_key, authors, CACHE_TTL)
    return authors

def fetch_and_filter(query: str,
                     only_women: bool=False,
                     year: str|None=None,
                     limit: int=DEFAULT_LIMIT
                    ) -> list[dict]:
    # 1) Initial search (include DOI)
    resp = requests.get(
        SEMANTIC_SCHOLAR_SEARCH,
        params={
            "query": query,
            "limit": limit,
            "fields": "title,abstract,authors,year,paperId,externalIds"
        },
        timeout=10
    )
    papers = resp.json().get("data", []) or []
    results = []

    for p in papers:
        title       = (p.get("title") or "").strip()
        abstract    = p.get("abstract") or "No abstract available."
        raw_authors = p.get("authors") or []
        year_val    = p.get("year")
        paper_id    = p.get("paperId")
        externalIds = p.get("externalIds", {})

        # 2) Year filter (fast)
        if year and str(year_val) != str(year):
            continue

        if not raw_authors:
            continue

        # 3) Quick pass on raw_authors to catch most cases:
        #    a) local whitelist  b) resolve_author_gender()
        has_woman = False
        gender_possible = False
        for a in raw_authors:
            first = a["name"].split()[0].lower()
            # whitelist
            if first in FEMALE_NAMES:
                has_woman = gender_possible = True
                break
            # ID‐based
            aid = a.get("authorId")
            if aid:
                gi = resolve_author_gender(aid)
                if gi:
                    gender_possible = True
                    if gi["gender"] == "female":
                        has_woman = True
                        break

        # 4) Only if still unresolved and all initials do we expand
        authors_raw = raw_authors
        if not gender_possible and all(len(a["name"].split()[0]) <= 2 for a in raw_authors):
            authors_raw = _expand_authors(paper_id, externalIds or {}, raw_authors)

        # 5) If expand changed authors, rerun quick pass
        if authors_raw is not raw_authors:
            has_woman = False
            gender_possible = False
            for a in authors_raw:
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

        # 6) Name‐based fallback with Genderize.io (capped)
        calls = 0
        if not has_woman and not gender_possible:
            for a in authors_raw:
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

        # 7) Skip definite all‐male
        if gender_possible and not has_woman:
            continue
        # strict women‐only
        if only_women and not has_woman:
            continue

        # 8) Build link + three‐state flag
        link = (
            f"https://www.semanticscholar.org/paper/{paper_id}"
            if paper_id else
            f"https://www.google.com/search?q={title.replace(' ', '+')}"
        )
        hwa = True if has_woman else "uncertain"

        results.append({
            "title":            title,
            "abstract":         abstract,
            "authors":          [a["name"] for a in authors_raw],
            "date":             f"{year_val}-01-01" if year_val else None,
            "has_woman_author": hwa,
            "link":             link,
        })

    return results
