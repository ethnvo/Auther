from api.models import Paper
from django.utils.dateparse import parse_date
import requests
from api.utils.resolve_author_gender import resolve_author_gender


SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
GENDERIZE_API = "https://api.genderize.io"
QUERY = "deer population"

def run():
    print(f"📚 Fetching papers for: {QUERY}")
    response = requests.get(SEMANTIC_SCHOLAR_API, params={
        "query": QUERY,
        "limit": 10,
        "fields": "title,abstract,authors,year,paperId"
    })

    papers = response.json().get("data", [])

    for paper in papers:
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        authors_raw = paper.get("authors", [])
        authors = [a["name"] for a in authors_raw]
        year = paper.get("year")
        paper_id = paper.get("paperId")

        url = f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else \
              f"https://www.google.com/search?q={title.replace(' ', '+')}"

        # Gender analysis
        genders = [resolve_author_gender(a["authorId"]) for a in authors_raw if a.get("authorId")]
        has_woman = any(g == "female" for g in genders if g is not None)
        gender_possible = any(g is not None for g in genders)

        # ❌ Skip if all are known and male
        if gender_possible and not has_woman:
            print(f"❌ Skipped: {title} (All authors male)")
            continue

        # ✅ Save paper
        Paper.objects.create(
            title=title,
            abstract=abstract or "No abstract available.",
            authors=authors,
            has_woman_author=has_woman,
            gender_inference_possible=gender_possible,
            date=parse_date(f"{year}-01-01") if year else None,
            link=url
        )

        tag = "✅ woman-led" if has_woman else "🔍 possible woman author (uncertain)"
        print(f"{tag}: {title}")
