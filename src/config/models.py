from __future__ import annotations

from pathlib import Path
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator


class RedditConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    credentials: Path = Field(default="", description="Path to Reddit API credentials file")
    subreddits: List[str] = Field(description="List of subreddits to scrape")
    pass


class ScraperConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reddit: Optional[RedditConfig] = Field(default=None)
    pass


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scraper: Optional[ScraperConfig] = Field(default=None)
