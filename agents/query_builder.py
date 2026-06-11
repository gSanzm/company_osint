from schemas.models import SearchQuery


def build_company_queries(
    company_name: str,
    company_website: str | None = None,
    country: str | None = None,
) -> list[SearchQuery]:
    """
    Genera búsquedas iniciales para investigar una empresa con fuentes abiertas.
    En esta primera versión no usamos LLM: son queries controladas y predecibles.
    """
    company_name = company_name.strip()
    company_website = (company_website or "").strip()
    country = (country or "").strip()

    context = f"{company_name} {country}".strip()

    queries = [
        SearchQuery(
            query=f"{context} official website",
            purpose="Encontrar la web oficial y descripción corporativa.",
        ),
        SearchQuery(
            query=f"{context} products services",
            purpose="Identificar productos, servicios y propuesta de valor.",
        ),
        SearchQuery(
            query=f"{context} competitors alternatives",
            purpose="Detectar competidores o alternativas.",
        ),
        SearchQuery(
            query=f"{context} reviews opinions",
            purpose="Encontrar señales reputacionales públicas.",
        ),
        SearchQuery(
            query=f"{context} news",
            purpose="Encontrar noticias recientes o menciones relevantes.",
        ),
    ]

    if company_website:
        domain = (
            company_website
            .replace("https://", "")
            .replace("http://", "")
            .replace("www.", "")
            .split("/")[0]
        )

        queries.insert(
            1,
            SearchQuery(
                query=f"site:{domain} {company_name}",
                purpose="Buscar información dentro del dominio oficial aportado por el usuario.",
            ),
        )

    return queries