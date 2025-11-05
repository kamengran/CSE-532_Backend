from pydantic import BaseModel
from typing import List, Optional

class RecommendQuery(BaseModel):
    genre: Optional[str] = None         # e.g., "RPG"
    platform: Optional[str] = None      # e.g., "PC"
    max_playtime: Optional[float] = None  # hours (e.g., 10)
    min_rating: Optional[float] = None  # e.g., 70
    keywords: Optional[str] = None      # free-text like "chill fast-paced"

class GameOut(BaseModel):
    title: str
    genres: List[str]
    platforms: List[str]
    playtime: Optional[float] = None
    rating: Optional[float] = None
    summary: Optional[str] = None
    score: float                         # similarity score

class Game(BaseModel):
    title: str
    genres: List[str]
    platforms: List[str]
    playtime: Optional[float] = None
    rating: Optional[float] = None
    summary: Optional[str] = None
    tags: List[str] = []
