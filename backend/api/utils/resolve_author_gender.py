# api/utils/resolve_author_gender.py

import os
import json
import requests

# Endpoints
SS_AUTHOR_URL = (
    "https://api.semanticscholar.org/graph/v1/author/{author_id}"
    "?fields=name,externalIds"
)
WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
GENDERIZE_API = "https://api.genderize.io"

# Cache path
CACHE_FILE = os.path.join(os.path.dirname(__file__), "author_verified_cache.json")

# Load or init cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE) as f:
        AUTHOR_CACHE = json.load(f)
else:
    AUTHOR_CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(AUTHOR_CACHE, f, indent=2)

def _parse_qid_from_uri(uri: str) -> str:
    return uri.rstrip("/").rsplit("/", 1)[-1]

def _query_wikidata_gender_by_qid(qid: str) -> str | None:
    """Query Wikidata by Q-ID for P21 (gender)."""
    query = f"""
    SELECT ?gender WHERE {{
      wd:{qid} wdt:P21 ?gender .
    }} LIMIT 1
    """
    resp = requests.get(
        WIKIDATA_SPARQL,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=10
    )
    if resp.status_code != 200:
        return None
    bindings = resp.json().get("results", {}).get("bindings", [])
    if not bindings:
        return None
    gender_uri = bindings[0]["gender"]["value"]
    gender_q = _parse_qid_from_uri(gender_uri)
    # Q6581072=female, Q6581097=male
    if gender_q == "Q6581072":
        return "female"
    if gender_q == "Q6581097":
        return "male"
    return None

def _query_wikidata_gender_by_label(name: str) -> str | None:
    """Query Wikidata by exact English rdfs:label for P21."""
    # escape quotes in name
    name_esc = name.replace('"', '\\"')
    query = f'''
    SELECT ?gender WHERE {{
      ?person wdt:P31 wd:Q5;             # instance of human
              rdfs:label "{name_esc}"@en;
              wdt:P21 ?gender .
    }} LIMIT 1
    '''
    resp = requests.get(
        WIKIDATA_SPARQL,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=10
    )
    if resp.status_code != 200:
        return None
    bindings = resp.json().get("results", {}).get("bindings", [])
    if not bindings:
        return None
    gender_uri = bindings[0]["gender"]["value"]
    gender_q = _parse_qid_from_uri(gender_uri)
    if gender_q == "Q6581072":
        return "female"
    if gender_q == "Q6581097":
        return "male"
    return None

def resolve_author_gender(author_id: str) -> dict[str,str] | None:
    """
    Returns {"gender": "female"|"male", "confidence": "verified"|"inferred"}
    or None if we cannot determine at all.
    """
    # 1) Cache hit
    if author_id in AUTHOR_CACHE:
        return AUTHOR_CACHE[author_id]

    # 2) Semantic Scholar lookup
    try:
        resp = requests.get(
            SS_AUTHOR_URL.format(author_id=author_id),
            timeout=10
        )
        if resp.status_code != 200:
            AUTHOR_CACHE[author_id] = None
            save_cache()
            return None
        info = resp.json()
    except Exception:
        AUTHOR_CACHE[author_id] = None
        save_cache()
        return None

    name = info.get("name", "")
    ext = info.get("externalIds", {}) or {}

    # 3) Wikidata via externalIds
    wikidata_q = ext.get("Wikidata") or ext.get("wikidataId")
    if wikidata_q:
        gender = _query_wikidata_gender_by_qid(wikidata_q)
        if gender:
            result = {"gender": gender, "confidence": "verified"}
            AUTHOR_CACHE[author_id] = result
            save_cache()
            return result

    # 4) Wikidata via label
    if name:
        gender = _query_wikidata_gender_by_label(name)
        if gender:
            result = {"gender": gender, "confidence": "verified"}
            AUTHOR_CACHE[author_id] = result
            save_cache()
            return result

    # 5) Fallback to Genderize.io on first name
    first = name.split()[0] if name else ""
    if len(first) > 2 and first.isalpha():
        try:
            gresp = requests.get(GENDERIZE_API, params={"name": first}, timeout=5)
            if gresp.status_code == 200:
                gender = gresp.json().get("gender")
                if gender in ("female", "male"):
                    result = {"gender": gender, "confidence": "inferred"}
                    AUTHOR_CACHE[author_id] = result
                    save_cache()
                    return result
        except Exception:
            pass

    # 6) Give up
    AUTHOR_CACHE[author_id] = None
    save_cache()
    return None
