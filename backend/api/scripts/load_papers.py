import requests
from api.utils.resolve_author_gender import resolve_author_gender

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
GENDERIZE_API = "https://api.genderize.io"
DEFAULT_LIMIT = 10  # Sweet spot - not too many, not too few
MAX_GENDERIZE_CALLS = 8  # Keep API calls reasonable

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
    results = []
    genderize_calls = 0  # Track API usage

    for paper in data:
        title      = (paper.get("title") or "").strip()
        abstract   = paper.get("abstract") or "No abstract available."
        authors_raw= paper.get("authors") or []
        year_val   = paper.get("year")
        paper_id   = paper.get("paperId")

        if not authors_raw:
            continue

        genders = []
        # 1) ID-based
        for a in authors_raw:
            aid = a.get("authorId")
            gi  = resolve_author_gender(aid) if aid else None
            if gi:
                # Store the author name with the gender info
                gi["name"] = a["name"]
                genders.append(gi)
        
        # 2) Name-based fallback for *all* authors where we have no gender yet
        for a in authors_raw:
            # Stop if we've hit our API limit
            if genderize_calls >= MAX_GENDERIZE_CALLS:
                break
                
            # skip if we already got something for that author
            if any(g for g in genders if g.get("name") == a["name"]):
                continue
            
            name_parts = a["name"].split()
            first = name_parts[0] if name_parts else ""
            
            # Skip initials and very short names
            if not first.isalpha() or len(first) <= 2:
                continue
                
            try:
                r = requests.get(GENDERIZE_API, params={"name": first}, timeout=5)
                genderize_calls += 1  # Increment counter
                if r.status_code == 200:
                    gender_data = r.json()
                    if gender_data.get("gender") in ["female", "male"]:
                        genders.append({
                            "gender": gender_data["gender"],
                            "confidence": "inferred",
                            "name": a["name"]
                        })
            except:
                pass

        has_woman      = any(g["gender"] == "female" for g in genders)
        has_man        = any(g["gender"] == "male" for g in genders)
        gender_possible= bool(genders)

        # Apply year filter
        if year and str(year_val) != str(year):
            continue
            
        # Keep papers that either:
        # 1. Have confirmed women authors, OR
        # 2. Have unknown gender (benefit of doubt for initials/unclear names)
        # Only exclude papers that are definitively all-male
        if gender_possible and not has_woman:
            continue
            
        # Apply only_women filter more strictly if requested
        if only_women and not has_woman:
            continue

        link = (f"https://www.semanticscholar.org/paper/{paper_id}"
                if paper_id else
                f"https://www.google.com/search?q={title.replace(' ', '+')}")

        results.append({
            "title": title,
            "abstract": abstract,
            "authors": [a["name"] for a in authors_raw],
            "date": f"{year_val}-01-01" if year_val else None,
            "has_woman_author": has_woman,
            "link": link,
        })

    return results