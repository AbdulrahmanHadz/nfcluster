import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from news_clustering.misc import json_dumps


class ArticleLocalModel(BaseModel):
    headline: Optional[str] = None
    description: Optional[str] = None
    article: Optional[str] = None
    author: Optional[str] = None
    keyword: Optional[str] = None
    url: str
    published_at: Optional[datetime] = None
    language: Optional[str] = None
    filename: Optional[str] = None
    publication: Optional[str] = None
    source_domain: Optional[str] = None

    @validator("keyword", pre=True, allow_reuse=True)
    def validate_keywords(cls, v):
        if isinstance(v, list):
            return json_dumps(v)
        return json_dumps([v])

    @validator("author", pre=True, allow_reuse=True)
    def validate_authors(cls, v):
        if isinstance(v, list):
            return json_dumps(v)
        return json_dumps([v])
