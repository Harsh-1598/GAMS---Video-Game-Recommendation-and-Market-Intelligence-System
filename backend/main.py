"""FastAPI entry point for the game recommendation website."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .engine import GameRecommendationEngine


ROOT = Path(__file__).resolve().parents[1]
engine = GameRecommendationEngine(ROOT / "vgsales.csv")

app = FastAPI(title="GAMS", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RecommendationRequest(BaseModel):
    played_game: str | None = Field(default=None, max_length=150)
    played_platform: str | None = None
    platform_mode: str = Field(default="any", pattern="^(any|same)$")
    selected_platform: str | None = None
    genre: str | None = None
    publisher: str | None = None
    release_decade: str | None = None
    limit: int = Field(default=10, ge=1, le=50)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "games": len(engine.data),
        "model": engine.model_name,
        "metrics": engine.metrics,
    }


@app.get("/api/options")
def options() -> dict:
    return engine.options()


@app.post("/api/recommend")
def recommend(request: RecommendationRequest) -> dict:
    try:
        return engine.recommend(
            title=request.played_game,
            played_platform=request.played_platform,
            platform_mode=request.platform_mode,
            selected_platform=request.selected_platform,
            genre=request.genre,
            publisher=request.publisher,
            release_decade=request.release_decade,
            limit=request.limit,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


FRONTEND_DIR = ROOT / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
