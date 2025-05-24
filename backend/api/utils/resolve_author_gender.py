import requests
import json
import os

SEMANTIC_SCHOLAR_AUTHOR_URL = "https://api.semanticscholar.org/graph/v1/author/{}?fields=name"
GENDERIZE_API = "https://api.genderize.io"
CACHE_FILE = "author_cache.json"

# Load cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        AUTHOR_CACHE = json.load(f)
else:
    AUTHOR_CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(AUTHOR_CACHE, f, indent=2)

def resolve_author_gender(author_id):
    if author_id in AUTHOR_CACHE:
        return AUTHOR_CACHE[author_id]  # cached result

    try:
        # Step 1: Get full name
        author_res = requests.get(SEMANTIC_SCHOLAR_AUTHOR_URL.format(author_id))
        if author_res.status_code != 200:
            return None
        name = author_res.json().get("name")
        if not name:
            return None

        first_name = name.split()[0]
        if len(first_name) <= 2:
            return None  # probably an initial

        # Step 2: Infer gender
        gender_res = requests.get(GENDERIZE_API, params={"name": first_name})
        if gender_res.status_code != 200:
            return None

        gender = gender_res.json().get("gender")
        AUTHOR_CACHE[author_id] = gender
        save_cache()

        return gender
    except Exception as e:
        print(f"❌ Error resolving gender for author {author_id}: {e}")
        return None
