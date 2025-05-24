import requests
from api.utils.resolve_author_gender import resolve_author_gender

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_PAPER  = "https://api.semanticscholar.org/graph/v1/paper"
OPENALEX_WORKS         = "https://api.openalex.org/works"
GENDERIZE_API          = "https://api.genderize.io"

DEFAULT_LIMIT       = 5
MAX_GENDERIZE_CALLS = 10

def fetch_and_filter(query: str, only_women=False, year=None, limit=DEFAULT_LIMIT):
    # 1) Initial search (now includes externalIds to grab DOI)
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
        authors_raw = p.get("authors") or []
        year_val    = p.get("year")
        paper_id    = p.get("paperId")
        externalIds = p.get("externalIds", {})

        if not authors_raw:
            continue

        # 2) If *all* authors are just initials, pull full info from SS detail
        all_initials = all(len(a["name"].split()[0]) <= 2 for a in authors_raw)
        if all_initials and paper_id:
            det = requests.get(
                f"{SEMANTIC_SCHOLAR_PAPER}/{paper_id}",
                params={"fields": "authors"},
                timeout=5
            )
            if det.ok:
                ss_auths = det.json().get("authors", []) or []
                authors_raw = [
                    {
                        "authorId": auth.get("author", {}).get("authorId"),
                        "name":     auth.get("author", {}).get("name")
                    }
                    for auth in ss_auths
                    if auth.get("author", {}).get("name")
                ]

        # 3) Still all initials? try OpenAlex by DOI
        all_initials = all(
            len(a["name"].split()[0]) <= 2
            for a in authors_raw
        )
        doi = externalIds.get("DOI")
        if all_initials and doi:
            oax = requests.get(f"{OPENALEX_WORKS}/doi:{doi}", timeout=5)
            if oax.ok:
                data = oax.json().get("authorships", [])
                authors_raw = [
                    {
                        "name": auth["author"]["display_name"],
                        "authorId": None
                    }
                    for auth in data
                    if auth.get("author", {}).get("display_name")
                ]

        # 4) Now run your gender‐detection loop
        has_woman = False
        gender_possible = False
        calls = 0

        for a in authors_raw:
            # ID‐based
            if a.get("authorId"):
                gi = resolve_author_gender(a["authorId"])
                if gi:
                    gender_possible = True
                    if gi["gender"] == "female":
                        has_woman = True
                        break
                    continue

            # Name‐based fallback
            first = a["name"].split()[0]
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

        # 5) Skip definite all‐male
        if gender_possible and not has_woman:
            continue
        # Year filter
        if year and str(year_val) != str(year):
            continue
        # Strict women‐only
        if only_women and not has_woman:
            continue

        # 6) Build the link
        link = (
            f"https://www.semanticscholar.org/paper/{paper_id}"
            if paper_id else
            f"https://www.google.com/search?q={title.replace(' ', '+')}"
        )

        # 7) Collect result
        results.append({
            "title":            title,
            "abstract":         abstract,
            "authors":          [a["name"] for a in authors_raw],
            "date":             f"{year_val}-01-01" if year_val else None,
            "has_woman_author": True if has_woman else "uncertain",
            "link":             link,
        })

    return results
