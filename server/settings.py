from __future__ import annotations
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "Osakana"
    DESCRIPTION: str = "「あとで読む」記事を管理できるWebアプリ"
    VERSION: str = "v0.1.0"

    ADDRESS: str = Field("localhost", env="API_ADDRESS")
    PORT: int = Field("8000", env="API_PORT")
    TIMEZONE: str = Field("Asia/Tokyo", env="TIMEZONE")
    ALLOWED_ORIGIN: str = Field("*", env="ALLOWED_ORIGIN")

    class Config:
        env_file: str = ".env"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        load_dotenv()

    @classmethod
    @lru_cache(maxsize=1)
    def get_settings(cls) -> Settings:
        return Settings()
