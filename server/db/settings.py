from __future__ import annotations
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    ADDRESS: str = Field(default="localhost", env="MS_ADDRESS")
    PORT: int = Field(default=7700, env="MS_PORT")

    class Config:
        env_file: str = ".env"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        load_dotenv()

    @classmethod
    @lru_cache(maxsize=1)
    def get_settings(cls) -> Settings:
        return Settings()
