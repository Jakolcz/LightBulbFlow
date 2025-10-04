from __future__ import annotations

from pathlib import Path
from typing import Literal, List
from pydantic import BaseModel, Field, ConfigDict, field_validator


class RedditConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    credentials: Path = Field(default="", description="Path to Reddit API credentials file")
    pass


class ScraperConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reddit: RedditConfig = Field(default_factory=RedditConfig)
    pass


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scraper: ScraperConfig = Field(default_factory=ScraperConfig)
