import requests
from api.utils.resolve_author_gender import resolve_author_gender
from api.utils.common_female_names import FEMALE_NAMES

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_PAPER  = "https://api.semanticscholar.org/graph/v1/paper"
OPENALEX_WORKS         = "https://api.openalex.org/works"
GENDERIZE_API          = "https://api.genderize.io"

DEFAULT_LIMIT       = 5
MAX_GENDERIZE_CALLS = 10

def fetch_and_filter(query: str, only_women=False, year=None, limit=DEFAULT_LIMIT):
    # 1) Initial search (grab DOI too)
    resp = requests.get(
        SEMANTIC_SCHOLAR_SEARCH,
        params={
            "query": query,
            "limit": limit,
            "fields": "title,abstract,authors,year,paperId,externalIds"
        },
        timeout=10,
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

        # Year filter (early exit)
        if year and str(year_val) != str(year):
            continue

        if not raw_authors:
            continue

        # 2) Expand authors via SS detail ➔ OpenAlex (omitted for brevity; keep your existing code)
        # authors_raw = _get_expanded_authors(paper_id, externalIds, raw_authors)
        authors_raw = raw_authors
        # [Insert your steps 2 & 3 here exactly as before to populate authors_raw]

        # 4) Gender detection with local whitelist
        has_woman = False
        gender_possible = False
        calls = 0

        for a in authors_raw:
            # a) ID-based
            if a.get("authorId"):
                gi = resolve_author_gender(a["authorId"])
                if gi:
                    gender_possible = True
                    if gi["gender"] == "female":
                        has_woman = True
                        break
                    continue

            # b) Local whitelist check
            first = a["name"].split()[0].lower()
            if first in FEMALE_NAMES:
                has_woman = True
                gender_possible = True
                break

            # c) Name-based fallback
            if first.isalpha() and len(first) > 2 and calls < MAX_GENDERIZE_CALLS:
                calls += 1
                try:
                    gr = requests.get(GENDERIZE_API, params={"name": first}, timeout=5)
                    if gr.ok:
                        gender = gr.json().get("gender")
                        if gender:
                            gender_possible = True
                            if gender == "female":
                                has_woman = True
                                break
                except requests.RequestException:
                    pass

        # 5) Skip definite all-male
        if gender_possible and not has_woman:
            continue
        # strict women-only filter
        if only_women and not has_woman:
            continue

        # 6) Build link & collect
        link = (
            f"https://www.semanticscholar.org/paper/{paper_id}"
            if paper_id else
            f"https://www.google.com/search?q={title.replace(' ', '+')}"
        )
        results.append({
            "title":            title,
            "abstract":         abstract,
            "authors":          [a["name"] for a in authors_raw],
            "date":             f"{year_val}-01-01" if year_val else None,
            "has_woman_author": bool(has_woman),
            "link":             link,
        })

    return results
