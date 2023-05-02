from datetime import date, datetime
from typing import Optional, Union, Literal

from pydantic import BaseModel, validator


DEFAULT_NUM_CLUSTERS = 13


def convert_list_string(list_to_convert: list):
    if isinstance(list_to_convert, list):
        return ", ".join(list_to_convert)
    return str(list_to_convert)


class SearchParamsLocalModel(BaseModel):
    q: Optional[str] = None
    qintitle: Optional[str] = "title"
    sources: Optional[str] = None
    domains: Optional[str] = None
    exclude_domains: Optional[str] = None
    from_param: Optional[Union[datetime, date]] = None
    to: Optional[Union[datetime, date]] = None
    language: Optional[str] = "en"
    region: Optional[str] = "GB"
    sort_by: Optional[Literal["relevancy", "popularity", "publishedAt"]] = "relevancy"
    num_pages: Optional[int] = 1
    page: Optional[int] = 1
    page_size: Optional[int] = None
    max_results: Optional[int] = 100

    _validate_sources = validator("sources", pre=True, allow_reuse=True)(
        convert_list_string
    )
    _validate_domains = validator("domains", pre=True, allow_reuse=True)(
        convert_list_string
    )
    _validate_exclude_domains = validator(
        "exclude_domains", pre=True, allow_reuse=True
    )(convert_list_string)

    @validator("language", pre=True)
    def validate_language(cls, v):
        if v not in [
            "ar",
            "de",
            "en",
            "es",
            "fr",
            "he",
            "it",
            "nl",
            "no",
            "pt",
            "ru",
            "sv",
            "ud",
            "zh",
        ]:
            return "en"
        return str(v)


class ClusterParamsLocalModel(SearchParamsLocalModel):
    num_clusters: int = DEFAULT_NUM_CLUSTERS
