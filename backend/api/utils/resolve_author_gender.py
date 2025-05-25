# api/utils/resolve_author_gender.py
import json
import os
from functools import lru_cache

import requests

# -------- Endpoints --------
SS_AUTHOR_URL = (
    "https://api.semanticscholar.org/graph/v1/author/{author_id}"
    "?fields=name,externalIds"
)
WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
GENDERIZE_API = "https://api.genderize.io"

# -------- File-based cache --------
CACHE_FILE = os.path.join(os.path.dirname(__file__), "author_verified_cache.json")

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        AUTHOR_CACHE: dict[str, dict | None] = json.load(f)
else:
    AUTHOR_CACHE: dict[str, dict | None] = {}


def _save_cache() -> None:
    """Persist AUTHOR_CACHE to disk."""
    with open(CACHE_FILE, "w") as f:
        json.dump(AUTHOR_CACHE, f, indent=2)


# -------- Helper functions --------
def _parse_qid_from_uri(uri: str) -> str:
    return uri.rstrip("/").rsplit("/", 1)[-1]


def _query_wikidata_gender_by_qid(qid: str) -> str | None:
    query = f"""
    SELECT ?gender WHERE {{
      wd:{qid} wdt:P21 ?gender .
    }} LIMIT 1
    """
    resp = requests.get(
        WIKIDATA_SPARQL,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=5,
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


def _query_wikidata_gender_by_label(name: str) -> str | None:
    name_esc = name.replace('"', '\\"')
    query = f'''
    SELECT ?gender WHERE {{
      ?person wdt:P31 wd:Q5;
              rdfs:label "{name_esc}"@en;
              wdt:P21 ?gender .
    }} LIMIT 1
    '''
    resp = requests.get(
        WIKIDATA_SPARQL,
        params={"query": query},
        headers={"Accept": "application/sparql-results+json"},
        timeout=5,
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


# -------- Uncached resolver (wrapped by lru_cache) --------
@lru_cache(maxsize=2048)
def _resolve_author_gender_uncached(author_id: str) -> dict[str, str] | None:
    """
    Heavy-weight resolver that queries external services.
    Returns {"gender": "female" or "male", "confidence": "verified" or "inferred"}
    or None if unknown.
    """
    # 1) Semantic Scholar
    try:
        resp = requests.get(
            SS_AUTHOR_URL.format(author_id=author_id),
            timeout=5,
        )
        if resp.status_code != 200:
            return None
        info = resp.json()
    except requests.RequestException:
        return None

    name = info.get("name", "")
    ext = info.get("externalIds") or {}

    # 2) Wikidata via externalIds
    wikidata_q = ext.get("Wikidata") or ext.get("wikidataId")
    if wikidata_q:
        gender = _query_wikidata_gender_by_qid(wikidata_q)
        if gender:
            return {"gender": gender, "confidence": "verified"}

    # 3) Wikidata via exact label
    if name:
        gender = _query_wikidata_gender_by_label(name)
        if gender:
            return {"gender": gender, "confidence": "verified"}

    # 4) Fallback to Genderize.io on first name
    first = name.split()[0] if name else ""
    if len(first) > 2 and first.isalpha():
        try:
            g_resp = requests.get(GENDERIZE_API, params={"name": first}, timeout=3)
            if g_resp.status_code == 200:
                g = g_resp.json().get("gender")
                if g in ("female", "male"):
                    return {"gender": g, "confidence": "inferred"}
        except requests.RequestException:
            pass

    # 5) Unknown
    return None


# -------- Public resolver --------
def resolve_author_gender(author_id: str) -> dict[str, str] | None:
    """
    Public entry point.
    First checks persistent disk cache, then defer to the lru-cached resolver.
    """
    if author_id in AUTHOR_CACHE:
        return AUTHOR_CACHE[author_id]

    result = _resolve_author_gender_uncached(author_id)
    AUTHOR_CACHE[author_id] = result
    _save_cache()
    return result
