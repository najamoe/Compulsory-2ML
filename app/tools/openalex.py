from typing import List, Dict, Optional
import requests

def search_papers(
    query: str,
    year: Optional[int] = None,
    min_citations: Optional[int] = None,
    limit: int = 5
) -> List[Dict]:

    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": 10
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("API ERROR:", response.text)
        return []

    data = response.json()

    results = []

    for paper in data.get("results", []):
        pub_year = paper.get("publication_year")
        citations = paper.get("cited_by_count", 0)

        if year and pub_year != year:
            continue

        if min_citations and citations < min_citations:
            continue

        location = paper.get("primary_location") or {}
        source = location.get("source") or {}

        url = source.get("homepage_url") or location.get("landing_page_url")

        results.append({
            "title": paper.get("title"),
            "authors": [a["author"]["display_name"] for a in paper.get("authorships", [])],
            "year": pub_year,
            "citations": citations,
            "url": url,
            "abstract": paper.get("abstract_inverted_index")
        })

        if len(results) >= limit:
            break

    return results