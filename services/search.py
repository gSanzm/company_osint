from tavily import TavilyClient

from schemas.models import SearchQuery, SearchResult
from utils.config import get_tavily_api_key


def search_tavily(
    query: SearchQuery,
    max_results: int = 5,
    search_depth: str = "basic",
) -> list[SearchResult]:
    """
    Ejecuta una búsqueda en Tavily y devuelve resultados normalizados.
    """
    client = TavilyClient(api_key=get_tavily_api_key())

    response = client.search(
        query=query.query,
        search_depth=search_depth,
        max_results=max_results,
        include_answer=False,
        include_raw_content=False,
    )

    results = []

    for item in response.get("results", []):
        title = item.get("title") or "Sin título"
        url = item.get("url")
        content = item.get("content")
        score = item.get("score")

        if not url:
            continue

        try:
            results.append(
                SearchResult(
                    title=title,
                    url=url,
                    content=content,
                    score=score,
                    query=query.query,
                    purpose=query.purpose,
                )
            )
        except Exception:
            continue

    return results


def run_company_search(
    queries: list[SearchQuery],
    max_results_per_query: int = 5,
) -> list[SearchResult]:
    """
    Ejecuta varias búsquedas y deduplica resultados por URL.
    """
    all_results: list[SearchResult] = []
    seen_urls: set[str] = set()

    for query in queries:
        query_results = search_tavily(
            query=query,
            max_results=max_results_per_query,
            search_depth="basic",
        )

        for result in query_results:
            url = str(result.url)

            if url in seen_urls:
                continue

            seen_urls.add(url)
            all_results.append(result)

    return all_results