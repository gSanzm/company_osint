from urllib.parse import urlparse

from schemas.models import SearchResult, RankedSource


NEWS_DOMAINS = [
    "elpais.com",
    "elmundo.es",
    "expansion.com",
    "cincodias.elpais.com",
    "eleconomista.es",
    "lavanguardia.com",
    "abc.es",
    "reuters.com",
    "bloomberg.com",
    "techcrunch.com",
]

REVIEW_DOMAINS = [
    "trustpilot.com",
    "ocu.org",
    "google.com",
    "tripadvisor.com",
    "g2.com",
    "capterra.com",
    "trust-radius.com",
]

SOCIAL_DOMAINS = [
    "linkedin.com",
    "x.com",
    "twitter.com",
    "facebook.com",
    "instagram.com",
    "youtube.com",
]

BUSINESS_DIRECTORY_DOMAINS = [
    "crunchbase.com",
    "linkedin.com/company",
    "einforma.com",
    "axesor.es",
    "kompass.com",
    "dnb.com",
]

SEO_AGGREGATOR_KEYWORDS = [
    "top",
    "best",
    "alternatives",
    "ranking",
    "comparativa",
    "mejores",
]


def get_domain(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc.lower().replace("www.", "")


def classify_source(result: SearchResult, company_website: str | None = None) -> tuple[str, str, str]:
    """
    Devuelve:
    - source_type
    - priority
    - reason
    """
    url = str(result.url)
    domain = get_domain(url)
    title = result.title.lower()
    content = (result.content or "").lower()
    text = f"{title} {content} {url.lower()}"

    official_domain = None
    if company_website:
        official_domain = get_domain(company_website)

    if official_domain and official_domain in domain:
        return (
            "official",
            "high",
            "El dominio coincide con la web oficial indicada por el usuario.",
        )

    if any(news_domain in domain for news_domain in NEWS_DOMAINS):
        return (
            "news",
            "medium",
            "La fuente parece ser un medio de comunicación o publicación informativa.",
        )

    if any(review_domain in domain for review_domain in REVIEW_DOMAINS):
        return (
            "reviews",
            "high",
            "La fuente parece contener opiniones, reseñas o valoraciones públicas.",
        )

    if any(social_domain in domain or social_domain in url.lower() for social_domain in SOCIAL_DOMAINS):
        return (
            "social",
            "medium",
            "La fuente parece ser una red social o perfil corporativo.",
        )

    if any(directory_domain in url.lower() for directory_domain in BUSINESS_DIRECTORY_DOMAINS):
        return (
            "business_directory",
            "medium",
            "La fuente parece ser un directorio empresarial o perfil corporativo.",
        )

    if "competitor" in text or "competidores" in text or "alternatives" in text or "alternativas" in text:
        return (
            "competitor",
            "medium",
            "La fuente parece estar relacionada con competidores o alternativas.",
        )

    if any(keyword in text for keyword in SEO_AGGREGATOR_KEYWORDS):
        return (
            "seo_aggregator",
            "low",
            "La fuente parece un agregador SEO o una página de ranking genérico.",
        )

    return (
        "unknown",
        "low",
        "No se ha podido clasificar con reglas simples.",
    )


def rank_sources(
    results: list[SearchResult],
    company_website: str | None = None,
) -> list[RankedSource]:
    ranked_sources = []

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    source_type_order = {
        "official": 0,
        "reviews": 1,
        "news": 2,
        "business_directory": 3,
        "social": 4,
        "competitor": 5,
        "unknown": 6,
        "seo_aggregator": 7,
    }

    for result in results:
        source_type, priority, reason = classify_source(
            result=result,
            company_website=company_website,
        )

        ranked_sources.append(
            RankedSource(
                title=result.title,
                url=result.url,
                content=result.content,
                score=result.score,
                query=result.query,
                purpose=result.purpose,
                source_type=source_type,
                priority=priority,
                reason=reason,
            )
        )

    ranked_sources.sort(
        key=lambda source: (
            priority_order.get(source.priority, 99),
            source_type_order.get(source.source_type, 99),
            -(source.score or 0),
        )
    )

    return ranked_sources