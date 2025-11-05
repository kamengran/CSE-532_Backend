from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pandas as pd

from app.models import RecommendQuery, GameOut, Game
from app.utils import load_games_csv, filter_df
from app.recommender import ContentRecommender



DATA_PATH = "data/games.csv"

app = FastAPI(title="Game Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Load and build model once at startup
df: pd.DataFrame = load_games_csv(DATA_PATH)
rec = ContentRecommender(df)



@app.get("/games", response_model=List[Game])
def list_games(
    genre: Optional[str] = None,
    platform: Optional[str] = None,
    max_playtime: Optional[float] = None,
    min_rating: Optional[float] = None,
    limit: int = Query(20, ge=1, le=100)
):
    out = filter_df(df, genre, platform, max_playtime, min_rating).head(limit)
    return [
        Game(
            title=row['title'],
            genres=row['genres_list'],
            platforms=row['platforms_list'],
            playtime=row['playtime'],
            rating=row['rating'],
            summary=row['summary'],
            tags=row['tags_list']
        )
        for _, row in out.iterrows()
    ]

@app.post("/recommend", response_model=List[GameOut])
def recommend(q: RecommendQuery):
    # 1) Filter by hard constraints first
    filtered = filter_df(df, q.genre, q.platform, q.max_playtime, q.min_rating)

    # 2) Build query text (keywords + genre/platform as soft hints)
    hints = []
    if q.genre: hints.append(q.genre)
    if q.platform: hints.append(q.platform)
    if q.keywords: hints.append(q.keywords)
    query_text = " ".join(hints) if hints else ""

    # 3) Run recommender on filtered set by temporarily swapping df
    if len(filtered) == 0:
        return []

    tmp_rec = ContentRecommender(filtered)
    top = tmp_rec.recommend(query_text, top_k=10)

    return [
        GameOut(
            title=row['title'],
            genres=row['genres_list'],
            platforms=row['platforms_list'],
            playtime=row['playtime'],
            rating=row['rating'],
            summary=row['summary'],
            score=float(row.get('score', 0.0))
        )
        for _, row in top.iterrows()
    ]
