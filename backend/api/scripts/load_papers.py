import requests
from api.utils.resolve_author_gender import resolve_author_gender

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
GENDERIZE_API = "https://api.genderize.io"
DEFAULT_LIMIT = 10

def fetch_and_filter(query: str,
                     only_women: bool = False,
                     year: str | None = None,
                     limit: int = DEFAULT_LIMIT) -> list[dict]:
    resp = requests.get(SEMANTIC_SCHOLAR_API, params={
        "query": query,
        "limit": limit,
        "fields": "title,abstract,authors,year,paperId"
    }, timeout=10)
    data = resp.json().get("data", []) or []
    results: list[dict] = []

    for paper in data:
        title = paper.get("title", "").strip()
        abstract = paper.get("abstract", "") or "No abstract available."
        authors_raw = paper.get("authors", []) or []
        year_val = paper.get("year")
        paper_id = paper.get("paperId")

        if not authors_raw:
            continue

        genders = []
        # 1) Try resolve_author_gender, then fallback to direct name check
        for a in authors_raw:
            author_id = a.get("authorId")
            gender_info = None
            if author_id:
                gender_info = resolve_author_gender(author_id)
            if gender_info:
                # got a verified/inferred gender by ID
                genders.append(gender_info)
                continue

            # name-based fallback for everyone else (or None from cache)
            first = a["name"].split()[0]
            if first.isalpha() and len(first) > 2:
                try:
                    gr = requests.get(GENDERIZE_API, params={"name": first}, timeout=5)
                    if gr.status_code == 200 and gr.json().get("gender") == "female":
                        genders.append({"gender": "female", "confidence": "inferred"})
                except Exception:
                    pass

        has_woman = any(g.get("gender") == "female" for g in genders)
        gender_possible = bool(genders)

        # skip all-male if we actually got any gender data
        if gender_possible and not has_woman:
            continue

        # year filter
        if year and str(year_val) != str(year):
            continue

        # only_women filter
        if only_women and not has_woman:
            continue

        link = (
            f"https://www.semanticscholar.org/paper/{paper_id}"
            if paper_id else
            f"https://www.google.com/search?q={title.replace(' ', '+')}"
        )

        results.append({
            "title": title,
            "abstract": abstract,
            "authors": [a["name"] for a in authors_raw],
            "date": f"{year_val}-01-01" if year_val else None,
            "has_woman_author": has_woman,
            "link": link,
        })

    return results
