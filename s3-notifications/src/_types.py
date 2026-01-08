from __future__ import annotations

from typing import TypedDict
from uuid import UUID


class Data(TypedDict):
    version: str
    status_code: int
    status_message: str
    time: str
    cost: float
    tasks_count: int
    tasks_error: int
    tasks: list[Task]


class Task(TypedDict):
    id: UUID
    status_code: int
    status_message: str
    time: str
    cost: float
    result_count: int
    path: list[str]
    data: _Data
    result: list[Result]


class _Data(TypedDict):
    api: str
    function: str
    se: str
    language_code: str
    location_code: int
    keywords: list[str]
    date_from: str


class Result(TypedDict):
    keyword: str
    spell: None
    location_code: int
    language_code: str
    search_partners: bool
    competition: str
    competition_index: int
    search_volume: int
    low_top_of_page_bid: float
    high_top_of_page_bid: float
    cpc: float
    monthly_searches: list[MonthlySearch]


class MonthlySearch(TypedDict):
    year: int
    month: int
    search_volume: int
