from pydantic import BaseModel, HttpUrl
from typing import Literal


class SearchQuery(BaseModel):
    query: str
    purpose: str


class SearchResult(BaseModel):
    title: str
    url: HttpUrl
    content: str | None = None
    score: float | None = None
    query: str
    purpose: str


SourceType = Literal[
    "official",
    "news",
    "reviews",
    "social",
    "business_directory",
    "competitor",
    "seo_aggregator",
    "unknown",
]


SourcePriority = Literal[
    "high",
    "medium",
    "low",
]


class RankedSource(BaseModel):
    title: str
    url: HttpUrl
    content: str | None = None
    score: float | None = None
    query: str
    purpose: str
    source_type: SourceType
    priority: SourcePriority
    reason: str