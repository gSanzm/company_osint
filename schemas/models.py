from pydantic import BaseModel, HttpUrl


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